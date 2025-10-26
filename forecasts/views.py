from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from core.models import League, Team, Match, Standing, Lineup, PlayerRating
from news.models import News


def home(request):
    """Головна сторінка - показуємо новини, ліги та матчі"""
    
    q = request.GET.get('q', '')
    
    leagues = League.objects.all()
    
    upcoming_matches = Match.objects.all().order_by('-date_utc')
    
    if q:
        upcoming_matches = upcoming_matches.filter(home_team__name__icontains=q) | \
                          upcoming_matches.filter(away_team__name__icontains=q)
    
    upcoming_matches = upcoming_matches[:20]
   
    featured_news = News.objects.all()[:5]
    latest_news = News.objects.all()[:10]
    
    context = {
        'leagues': leagues,
        'upcoming': upcoming_matches,
        'featured': featured_news,
        'latest_news': latest_news,
        'q': q,
    }
    
    return render(request, 'home.html', context)


def league_detail(request, league_id):
    """Сторінка конкретної ліги - таблиця та матчі"""
    
    # Знаходимо лігу або показуємо 404
    league = get_object_or_404(League, id=league_id)
    
    # Отримуємо турнірну таблицю, сортуємо за очками
    standings = Standing.objects.filter(league=league).order_by('-points')
    
    # Отримуємо всі матчі ліги
    matches = Match.objects.filter(league=league).order_by('date_utc')
    
    context = {
        'league': league,
        'standings': standings,
        'matches': matches
    }
    
    return render(request, 'league_detail.html', context)


def team_detail(request, team_id):
    """Сторінка конкретної команди - інформація та матчі"""
    
    # Знаходимо команду або показуємо 404
    team = get_object_or_404(Team, id=team_id)
    
    # Знаходимо всі матчі команди (де вона грає вдома АБО в гостях)
    home_matches = Match.objects.filter(home_team=team)
    away_matches = Match.objects.filter(away_team=team)
    
    # Об'єднуємо матчі та беремо перші 10
    all_matches = (home_matches | away_matches).order_by('-date_utc')[:10]
    
    context = {
        'team': team,
        'matches': all_matches
    }
    
    return render(request, 'team_detail.html', context)


def match_detail(request, match_id):
    """Сторінка конкретного матчу - детальна інформація"""
    
    # Знаходимо матч або показуємо 404
    match = get_object_or_404(Match, id=match_id)
    
    # Отримуємо склади команд
    home_lineup = Lineup.objects.filter(match=match, team=match.home_team)
    away_lineup = Lineup.objects.filter(match=match, team=match.away_team)
    
    # Отримуємо топ-5 гравців за рейтингом
    top_ratings = PlayerRating.objects.filter(match=match).order_by('-rating')[:5]
    
    context = {
        'match': match,
        'home_lineup': home_lineup,
        'away_lineup': away_lineup,
        'top_ratings': top_ratings
    }
    
    return render(request, 'match_detail.html', context)


def matches_list(request):
    """Список всіх матчів - майбутні та минулі"""
    
    # Отримуємо поточний час
    now = timezone.now()
    
    # Майбутні матчі (дата більше або дорівнює зараз)
    upcoming = Match.objects.filter(date_utc__gte=now).order_by('date_utc')[:50]
    
    # Минулі матчі (дата менше зараз), сортуємо від нових до старих
    recent = Match.objects.filter(date_utc__lt=now).order_by('-date_utc')[:50]
    
    context = {
        'upcoming': upcoming,
        'recent': recent
    }
    
    return render(request, 'matches.html', context)


def tables_view(request):
    """Турнірні таблиці всіх ліг"""
    
    # Отримуємо всі ліги
    leagues = League.objects.all()
    
    # Створюємо список для таблиць
    tables = []
    
    # Для кожної ліги отримуємо топ-10 команд
    for league in leagues:
        # Шукаємо турнірну таблицю ліги
        standings = Standing.objects.filter(league=league).order_by('-points')[:10]
        
        # Якщо є дані - додаємо до списку
        if standings.exists():
            tables.append({
                'league': league,
                'standings': standings
            })
    
    return render(request, 'tables.html', {'tables': tables})


def analytics_view(request):
    """Сторінка з аналітикою - топ команди"""
    
    # Отримуємо топ-10 команд за очками
    top_teams = Standing.objects.order_by('-points')[:10]
    
    return render(request, 'analytics.html', {'top_teams': top_teams})


def contacts_view(request):
    """Сторінка контактів"""
    return render(request, 'contacts.html')
