FootyForecast (Django)

Quickstart

1. Create venv and install deps (already done in this project):
   - Windows PowerShell:
     .\.venv\Scripts\python.exe -m pip install -r requirements.txt (optional)

2. Create static dir (optional to silence warning):
```
mkdir static
```

3. Run migrations and start server:
```
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe manage.py createsuperuser
.\.venv\Scripts\python.exe manage.py runserver
```

4. Import CSVs:
```
.\.venv\Scripts\python.exe manage.py import_csv --matches path\to\matches.csv --results path\to\results.csv --standings path\to\standings.csv
.\.venv\Scripts\python.exe manage.py recompute_forecasts
```

CSV formats

- matches.csv: match_id,season,league,date_utc,home_team,away_team,round,stadium
- results.csv: match_id,home_goals,away_goals,status
- standings.csv: league,team,played,won,draw,lost,gf,ga,points,home_played,away_played
- odds.csv: match_id,book,ts,home_odds,draw_odds,away_odds
- events.csv: match_id,stat_name,value

Pages

- / — Home: leagues and upcoming matches
- /league/<id>/ — League page with table and fixtures
- /team/<id>/ — Team recent matches
- /match/<id>/ — Match detail with forecast

Admin

- /admin — manage data and flags

API Docs

- /api/schema/ (OpenAPI)
- /api/docs/ (Swagger UI)

Notes

- Probabilities sum to 1.0 (displayed as 0-1); confidence is low/medium/high by spread.
- If data is missing, do not publish the match (toggle in Admin).

