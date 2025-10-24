from django.core.management.base import BaseCommand
from core.models import League, Team, Standing


LEAGUES = {
    "Українська Прем’єр-ліга": {
        "country": "Україна",
        "code": "UPL",
        "teams": [
            "Dynamo Kyiv","Shakhtar Donetsk","Oleksandriya","Polissya Zhytomyr","Kryvbas Kryvyi Rih","Karpaty Lviv","Zorya Luhansk","Rukh Lviv","Veres Rivne","Kolos Kovalivka","Obolon Kyiv","LNZ Cherkasy","Epitsentr Kamianets-Podilskyi","SC Poltava","Metalist 1925 Kharkiv","Kudrivka",
        ],
    },
    "Premier League": {
        "country": "England",
        "code": "EPL",
        "teams": [
            "Arsenal","Manchester City","Liverpool","Chelsea","Tottenham Hotspur","Manchester United","Newcastle United","Aston Villa","West Ham United","Brighton & Hove Albion","Brentford","Wolverhampton Wanderers","Crystal Palace","Everton","Fulham","Nottingham Forest","Leeds United","Burnley","AFC Bournemouth","Southampton",
        ],
    },
    "LaLiga": {
        "country": "Spain",
        "code": "LL",
        "teams": [
            "Real Madrid","Barcelona","Atlético Madrid","Real Sociedad","Athletic Club Bilbao","Real Betis","Villarreal","Girona","Valencia","Celta Vigo","Osasuna","Mallorca","Las Palmas","Getafe","Sevilla","Deportivo Alavés","Rayo Vallecano","Real Valladolid","Leganés","Espanyol",
        ],
    },
    "Bundesliga": {
        "country": "Germany",
        "code": "BUN",
        "teams": [
            "Bayern Munich","Borussia Dortmund","RB Leipzig","Bayer Leverkusen","Eintracht Frankfurt","VfL Wolfsburg","SC Freiburg","Borussia Mönchengladbach","FC Union Berlin","VfB Stuttgart","Mainz 05","Werder Bremen","FC Augsburg","TSG Hoffenheim","FC Köln","VfL Bochum","Fortuna Düsseldorf","FC St. Pauli",
        ],
    },
    "Serie A": {
        "country": "Italy",
        "code": "SA",
        "teams": [
            "Inter Milan","AC Milan","Juventus","Napoli","Roma","Lazio","Atalanta","Fiorentina","Bologna","Torino","Udinese","Monza","Genoa","Cagliari","Empoli","Lecce","Verona","Venezia","Parma","Como",
        ],
    },
    "Ligue 1": {
        "country": "France",
        "code": "L1",
        "teams": [
            "Paris Saint-Germain","Olympique de Marseille","AS Monaco","Lille OSC","Olympique Lyonnais","Stade Rennais","RC Lens","OGC Nice","Toulouse","Reims","Montpellier","Nantes","Strasbourg","Brest","Lorient","Metz","Auxerre","Le Havre",
        ],
    },
    "Eredivisie": {
        "country": "Netherlands",
        "code": "NED",
        "teams": [
            "Ajax","PSV Eindhoven","Feyenoord","AZ Alkmaar","FC Twente","SC Heerenveen","FC Utrecht","Sparta Rotterdam","NEC Nijmegen","Vitesse","FC Groningen","PEC Zwolle","RKC Waalwijk","Go Ahead Eagles","Fortuna Sittard","Almere City","Heracles Almelo","Excelsior",
        ],
    },
    "Primeira Liga": {
        "country": "Portugal",
        "code": "POR",
        "teams": [
            "FC Porto","SL Benfica","Sporting CP","SC Braga","Vitória Guimarães","Boavista","Estoril Praia","Rio Ave","Casa Pia","Gil Vicente","Famalicão","Moreirense","Portimonense","Farense","Vizela","Estrela Amadora","Chaves","Arouca",
        ],
    },
    "Європа – Кваліфікація ЧС 2026": {
        "country": "Europe",
        "code": "UEFA-WCQ26",
        "teams": [
            # Національні збірні можна додати окремим CSV; створюємо лише лігу
        ],
    },
}


class Command(BaseCommand):
    help = "Seed demo leagues, teams and empty standings for 2025/26"

    def add_arguments(self, parser):
        parser.add_argument('--season', default='2025/26')

    def handle(self, *args, **opts):
        season = opts['season']
        created_leagues = 0
        created_teams = 0
        created_rows = 0
        for name, meta in LEAGUES.items():
            league, created = League.objects.get_or_create(code=meta['code'], defaults={'name': name, 'country': meta['country'], 'is_active': True})
            if created:
                created_leagues += 1
            for t in meta['teams']:
                team, t_created = Team.objects.get_or_create(name=t, league=league)
                if t_created:
                    created_teams += 1
                # ensure standings row exists
                st, s_created = Standing.objects.get_or_create(league=league, team=team, defaults={
                    'played': 0, 'won': 0, 'draw': 0, 'lost': 0, 'gf': 0, 'ga': 0, 'points': 0,
                    'home_played': 0, 'away_played': 0,
                })
                if s_created:
                    created_rows += 1
        self.stdout.write(self.style.SUCCESS(f"Seeded leagues={created_leagues}, teams={created_teams}, standings_rows={created_rows} for season {season}"))

