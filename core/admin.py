from django.contrib import admin
from .models import League, Team, Match, Result, Standing, Odds, Event, Player, Lineup, PlayerRating


@admin.register(League)
class LeagueAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'is_active')
    list_filter = ('country', 'is_active')
    search_fields = ('name', 'code')


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'league')
    search_fields = ('name',)
    list_filter = ('league',)


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ('match_id', 'league', 'season', 'date_utc', 'home_team', 'away_team', 'is_published')
    search_fields = ('match_id', 'home_team__name', 'away_team__name')
    list_filter = ('league', 'season', 'is_published')
    date_hierarchy = 'date_utc'


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ('match', 'home_goals', 'away_goals', 'status')
    list_filter = ('status',)


@admin.register(Standing)
class StandingAdmin(admin.ModelAdmin):
    list_display = ('league', 'team', 'points', 'played', 'won', 'draw', 'lost')
    list_filter = ('league',)


@admin.register(Odds)
class OddsAdmin(admin.ModelAdmin):
    list_display = ('match', 'book', 'ts', 'home_odds', 'draw_odds', 'away_odds')
    list_filter = ('book',)
    date_hierarchy = 'ts'


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('match', 'stat_name', 'value')
    list_filter = ('stat_name',)


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('name', 'team', 'position')
    search_fields = ('name',)
    list_filter = ('team', 'position')


@admin.register(Lineup)
class LineupAdmin(admin.ModelAdmin):
    list_display = ('match', 'team', 'player', 'is_starting', 'shirt_number')
    list_filter = ('team', 'is_starting')


@admin.register(PlayerRating)
class PlayerRatingAdmin(admin.ModelAdmin):
    list_display = ('match', 'team', 'player', 'rating')
    list_filter = ('team',)
