from django.shortcuts import get_object_or_404, render
from django.db.models import Q
from django.utils import timezone
from core.models import League, Team, Match, Standing, Lineup, PlayerRating
from news.models import News


def home(request):
    q = request.GET.get('q', '').strip()
    leagues = League.objects.filter(is_active=True).order_by('country', 'name')
    matches = Match.objects.select_related('home_team', 'away_team', 'league').order_by('date_utc')
    if q:
        matches = matches.filter(Q(home_team__name__icontains=q) | Q(away_team__name__icontains=q) | Q(league__name__icontains=q))
    upcoming = matches[:30]
    featured = News.objects.filter(is_featured=True)[:5]
    latest_news = News.objects.all()[:9]
    return render(request, 'home.html', {'leagues': leagues, 'upcoming': upcoming, 'q': q, 'featured': featured, 'latest_news': latest_news})


def league_detail(request, league_id: int):
    league = get_object_or_404(League, id=league_id)
    standings = Standing.objects.filter(league=league).select_related('team').order_by('-points', '-gf')
    matches = Match.objects.filter(league=league).order_by('date_utc')[:100]
    return render(request, 'league_detail.html', {'league': league, 'standings': standings, 'matches': matches})


def team_detail(request, team_id: int):
    team = get_object_or_404(Team, id=team_id)
    recent_home = team.home_matches.select_related('league', 'away_team').order_by('-date_utc')[:5]
    recent_away = team.away_matches.select_related('league', 'home_team').order_by('-date_utc')[:5]
    return render(request, 'team_detail.html', {'team': team, 'recent_home': recent_home, 'recent_away': recent_away})


def matches_list(request):
    q = request.GET.get('q', '').strip()
    matches = Match.objects.select_related('home_team', 'away_team', 'league').order_by('date_utc')
    if q:
        matches = matches.filter(Q(home_team__name__icontains=q) | Q(away_team__name__icontains=q) | Q(league__name__icontains=q))
    upcoming = matches.filter(date_utc__gte=timezone.now())[:50]
    recent = matches.filter(date_utc__lt=timezone.now()).order_by('-date_utc')[:50]
    return render(request, 'matches.html', {'upcoming': upcoming, 'recent': recent, 'q': q})


def match_detail(request, match_id: int):
    match = get_object_or_404(Match.objects.select_related('home_team', 'away_team', 'league'), id=match_id)
    home_lineup = Lineup.objects.filter(match=match, team=match.home_team, is_starting=True).select_related('player').order_by('shirt_number')
    away_lineup = Lineup.objects.filter(match=match, team=match.away_team, is_starting=True).select_related('player').order_by('shirt_number')
    top_ratings = PlayerRating.objects.filter(match=match).select_related('player', 'team').order_by('-rating')[:6]
    return render(request, 'match_detail.html', {'match': match, 'home_lineup': home_lineup, 'away_lineup': away_lineup, 'top_ratings': top_ratings})


def tables_view(request):
    """Турнірні таблиці всіх ліг"""
    q = request.GET.get('q', '').strip()
    leagues = League.objects.filter(is_active=True).order_by('country', 'name')
    if q:
        leagues = leagues.filter(Q(name__icontains=q) | Q(country__icontains=q))
    
    # Отримуємо таблиці для кожної ліги
    tables_data = []
    for league in leagues:
        standings = Standing.objects.filter(league=league).select_related('team').order_by('-points', '-gf')[:10]
        if standings:
            tables_data.append({
                'league': league,
                'standings': standings
            })
    
    return render(request, 'tables.html', {'tables_data': tables_data, 'q': q})


def analytics_view(request):
    """Аналітика та статистика"""
    # Топ команди по очкам
    top_teams = Standing.objects.select_related('team', 'league').order_by('-points')[:10]
    
    # Найближчі матчі з високою впевненістю прогнозу
    upcoming_matches = Match.objects.select_related('home_team', 'away_team', 'league', 'forecast').filter(
        date_utc__gte=timezone.now(),
        forecast__isnull=False
    ).order_by('date_utc')[:20]
    
    # Статистика по лігам
    leagues_stats = []
    for league in League.objects.filter(is_active=True):
        matches_count = Match.objects.filter(league=league).count()
        teams_count = Standing.objects.filter(league=league).count()
        leagues_stats.append({
            'league': league,
            'matches': matches_count,
            'teams': teams_count
        })
    
    return render(request, 'analytics.html', {
        'top_teams': top_teams,
        'upcoming_matches': upcoming_matches,
        'leagues_stats': leagues_stats
    })


def contacts_view(request):
    """Контактна інформація"""
    return render(request, 'contacts.html')