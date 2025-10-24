from __future__ import annotations

from dataclasses import dataclass
from typing import List, Tuple

from django.db.models import Avg
from core.models import Match, Result, Standing
from .models import Forecast


@dataclass
class Factor:
    name: str
    weight: float
    detail: str


def _softmax3(a: float, b: float, c: float) -> Tuple[float, float, float]:
    s = a + b + c
    if s <= 0:
        return 1 / 3, 1 / 3, 1 / 3
    return a / s, b / s, c / s


def compute_forecast(match: Match) -> Forecast:
    # Rule-based: standings points and recent goal difference
    home_st = Standing.objects.filter(league=match.league, team=match.home_team).first()
    away_st = Standing.objects.filter(league=match.league, team=match.away_team).first()

    # recent form: last 5 per team
    recent_home = list(match.home_team.home_matches.order_by('-date_utc')[:5])
    recent_away = list(match.away_team.away_matches.order_by('-date_utc')[:5])

    def goal_diff(ms: List[Match]) -> float:
        diffs = []
        for m in ms:
            if hasattr(m, 'result'):
                diffs.append(m.result.home_goals - m.result.away_goals if m.home_team_id == match.home_team_id else m.result.away_goals - m.result.home_goals)
        return sum(diffs) / len(diffs) if diffs else 0.0

    score_home = 0.0
    score_draw = 0.5
    score_away = 0.0
    factors: List[Factor] = []

    if home_st and away_st:
        delta_pts = (home_st.points - away_st.points) / max(1, home_st.played + away_st.played)
        score_home += 0.6 + 0.8 * max(0.0, delta_pts)
        score_away += 0.6 + 0.8 * max(0.0, -delta_pts)
        factors.append(Factor('table_position', 0.8, f"Δpts_norm={delta_pts:.2f}"))

    gd_home = goal_diff(recent_home)
    gd_away = goal_diff(recent_away)
    score_home += 0.4 + 0.5 * max(0.0, gd_home)
    score_away += 0.4 + 0.5 * max(0.0, -gd_home)
    score_away += 0.4 + 0.5 * max(0.0, gd_away)
    score_home += 0.4 + 0.5 * max(0.0, -gd_away)
    factors.append(Factor('recent_form', 0.6, f"gd_home={gd_home:.2f}, gd_away={gd_away:.2f}"))

    pH, pD, pA = _softmax3(score_home, score_draw, score_away)

    # confidence by spread
    top = max(pH, pD, pA)
    if top >= 0.6:
        conf = 'high'
    elif top >= 0.45:
        conf = 'medium'
    else:
        conf = 'low'

    fc, _ = Forecast.objects.update_or_create(
        match=match,
        defaults={
            'prob_home': round(pH, 4),
            'prob_draw': round(pD, 4),
            'prob_away': round(pA, 4),
            'confidence': conf,
            'explain': [{'name': f.name, 'weight': f.weight, 'detail': f.detail} for f in factors],
        },
    )
    return fc

