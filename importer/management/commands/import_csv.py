import csv
from datetime import datetime
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils.timezone import make_aware
from core.models import League, Team, Match, Result, Standing, Odds, Event, Player, Lineup, PlayerRating


class Command(BaseCommand):
    help = 'Import CSV files: matches, results, standings, odds, events'

    def add_arguments(self, parser):
        parser.add_argument('--matches', type=str)
        parser.add_argument('--results', type=str)
        parser.add_argument('--standings', type=str)
        parser.add_argument('--odds', type=str)
        parser.add_argument('--events', type=str)
        parser.add_argument('--lineups', type=str)
        parser.add_argument('--ratings', type=str)

    def handle(self, *args, **options):
        with transaction.atomic():
            if options.get('matches'):
                self.import_matches(options['matches'])
            if options.get('results'):
                self.import_results(options['results'])
            if options.get('standings'):
                self.import_standings(options['standings'])
            if options.get('odds'):
                self.import_odds(options['odds'])
            if options.get('events'):
                self.import_events(options['events'])
            if options.get('lineups'):
                self.import_lineups(options['lineups'])
            if options.get('ratings'):
                self.import_ratings(options['ratings'])
        self.stdout.write(self.style.SUCCESS('Import completed'))

    def import_matches(self, path: str):
        with open(path, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            required = {'match_id', 'season', 'league', 'date_utc', 'home_team', 'away_team', 'round'}
            missing = required - set(reader.fieldnames or [])
            if missing:
                raise CommandError(f"matches.csv missing columns: {missing}")
            for i, row in enumerate(reader, start=2):
                league, _ = League.objects.get_or_create(code=row['league'], defaults={'name': row['league']})
                home, _ = Team.objects.get_or_create(name=row['home_team'], league=league)
                away, _ = Team.objects.get_or_create(name=row['away_team'], league=league)
                try:
                    dt = make_aware(datetime.fromisoformat(row['date_utc']))
                except Exception as e:
                    raise CommandError(f"matches.csv line {i}: bad date_utc {row['date_utc']} ({e})")
                Match.objects.update_or_create(
                    match_id=row['match_id'],
                    defaults={
                        'season': row['season'],
                        'league': league,
                        'date_utc': dt,
                        'round': row.get('round') or '',
                        'stadium': row.get('stadium') or '',
                        'home_team': home,
                        'away_team': away,
                    },
                )

    def import_results(self, path: str):
        with open(path, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            required = {'match_id', 'home_goals', 'away_goals', 'status'}
            missing = required - set(reader.fieldnames or [])
            if missing:
                raise CommandError(f"results.csv missing columns: {missing}")
            for i, row in enumerate(reader, start=2):
                try:
                    match = Match.objects.get(match_id=row['match_id'])
                except Match.DoesNotExist:
                    raise CommandError(f"results.csv line {i}: match_id {row['match_id']} not found")
                Result.objects.update_or_create(
                    match=match,
                    defaults={
                        'home_goals': int(row['home_goals']),
                        'away_goals': int(row['away_goals']),
                        'status': row['status'],
                    },
                )

    def import_standings(self, path: str):
        with open(path, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            required = {'league', 'team', 'played', 'won', 'draw', 'lost', 'gf', 'ga', 'points'}
            missing = required - set(reader.fieldnames or [])
            if missing:
                raise CommandError(f"standings.csv missing columns: {missing}")
            for i, row in enumerate(reader, start=2):
                league, _ = League.objects.get_or_create(code=row['league'], defaults={'name': row['league']})
                team, _ = Team.objects.get_or_create(name=row['team'], league=league)
                Standing.objects.update_or_create(
                    league=league, team=team,
                    defaults={
                        'played': int(row['played']),
                        'won': int(row['won']),
                        'draw': int(row['draw']),
                        'lost': int(row['lost']),
                        'gf': int(row['gf']),
                        'ga': int(row['ga']),
                        'points': int(row['points']),
                        'home_played': int(row.get('home_played') or 0),
                        'away_played': int(row.get('away_played') or 0),
                    },
                )

    def import_odds(self, path: str):
        with open(path, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            required = {'match_id', 'book', 'ts', 'home_odds', 'draw_odds', 'away_odds'}
            missing = required - set(reader.fieldnames or [])
            if missing:
                raise CommandError(f"odds.csv missing columns: {missing}")
            for i, row in enumerate(reader, start=2):
                try:
                    match = Match.objects.get(match_id=row['match_id'])
                except Match.DoesNotExist:
                    raise CommandError(f"odds.csv line {i}: match_id {row['match_id']} not found")
                try:
                    ts = make_aware(datetime.fromisoformat(row['ts']))
                except Exception as e:
                    raise CommandError(f"odds.csv line {i}: bad ts {row['ts']} ({e})")
                Odds.objects.update_or_create(
                    match=match, book=row['book'], ts=ts,
                    defaults={
                        'home_odds': float(row['home_odds']),
                        'draw_odds': float(row['draw_odds']),
                        'away_odds': float(row['away_odds']),
                    },
                )

    def import_events(self, path: str):
        with open(path, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            required = {'match_id', 'stat_name', 'value'}
            missing = required - set(reader.fieldnames or [])
            if missing:
                raise CommandError(f"events.csv missing columns: {missing}")
            for i, row in enumerate(reader, start=2):
                try:
                    match = Match.objects.get(match_id=row['match_id'])
                except Match.DoesNotExist:
                    raise CommandError(f"events.csv line {i}: match_id {row['match_id']} not found")
                Event.objects.update_or_create(
                    match=match, stat_name=row['stat_name'],
                    defaults={'value': float(row['value'])},
                )

    def import_lineups(self, path: str):
        with open(path, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            required = {'match_id', 'team', 'player', 'position', 'is_starting', 'shirt_number'}
            missing = required - set(reader.fieldnames or [])
            if missing:
                raise CommandError(f"lineups.csv missing columns: {missing}")
            for i, row in enumerate(reader, start=2):
                try:
                    match = Match.objects.get(match_id=row['match_id'])
                except Match.DoesNotExist:
                    raise CommandError(f"lineups.csv line {i}: match_id {row['match_id']} not found")
                team = Team.objects.filter(name=row['team'], league=match.league).first()
                if not team:
                    raise CommandError(f"lineups.csv line {i}: team {row['team']} not in league {match.league}")
                player, _ = Player.objects.get_or_create(name=row['player'], team=team, defaults={'position': row.get('position') or ''})
                Lineup.objects.update_or_create(
                    match=match, player=player,
                    defaults={
                        'team': team,
                        'is_starting': row['is_starting'].strip().lower() in ('1', 'true', 'yes', 'y'),
                        'shirt_number': int(row['shirt_number']) if row.get('shirt_number') else None,
                    },
                )

    def import_ratings(self, path: str):
        with open(path, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            required = {'match_id', 'team', 'player', 'rating'}
            missing = required - set(reader.fieldnames or [])
            if missing:
                raise CommandError(f"ratings.csv missing columns: {missing}")
            for i, row in enumerate(reader, start=2):
                try:
                    match = Match.objects.get(match_id=row['match_id'])
                except Match.DoesNotExist:
                    raise CommandError(f"ratings.csv line {i}: match_id {row['match_id']} not found")
                team = Team.objects.filter(name=row['team'], league=match.league).first()
                if not team:
                    raise CommandError(f"ratings.csv line {i}: team {row['team']} not in league {match.league}")
                player, _ = Player.objects.get_or_create(name=row['player'], team=team)
                PlayerRating.objects.update_or_create(
                    match=match, player=player,
                    defaults={'team': team, 'rating': float(row['rating'])},
                )

