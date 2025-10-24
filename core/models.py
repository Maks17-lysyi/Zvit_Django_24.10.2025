from django.db import models


class League(models.Model):
    code = models.CharField(max_length=50)
    name = models.CharField(max_length=200)
    country = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('code', 'name')
        ordering = ['country', 'name']

    def __str__(self) -> str:
        return f"{self.name}"


class Team(models.Model):
    name = models.CharField(max_length=200)
    league = models.ForeignKey(League, on_delete=models.CASCADE, related_name='teams')

    class Meta:
        unique_together = ('name', 'league')
        ordering = ['name']

    def __str__(self) -> str:
        return self.name


class Match(models.Model):
    match_id = models.CharField(max_length=64, unique=True)
    season = models.CharField(max_length=20)
    league = models.ForeignKey(League, on_delete=models.CASCADE, related_name='matches')
    date_utc = models.DateTimeField()
    round = models.CharField(max_length=50, blank=True)
    stadium = models.CharField(max_length=200, blank=True)
    home_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='home_matches')
    away_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='away_matches')
    is_published = models.BooleanField(default=True)

    class Meta:
        indexes = [
            models.Index(fields=['date_utc']),
            models.Index(fields=['league', 'season']),
        ]
        ordering = ['date_utc']

    def __str__(self) -> str:
        return f"{self.home_team} vs {self.away_team} ({self.date_utc.date()})"


class Result(models.Model):
    match = models.OneToOneField(Match, on_delete=models.CASCADE, related_name='result')
    home_goals = models.IntegerField()
    away_goals = models.IntegerField()
    status = models.CharField(max_length=20, choices=[('finished', 'finished'), ('postponed', 'postponed')])

    def __str__(self) -> str:
        return f"{self.match}: {self.home_goals}-{self.away_goals}"


class Standing(models.Model):
    league = models.ForeignKey(League, on_delete=models.CASCADE, related_name='standings')
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    played = models.IntegerField(default=0)
    won = models.IntegerField(default=0)
    draw = models.IntegerField(default=0)
    lost = models.IntegerField(default=0)
    gf = models.IntegerField(default=0)
    ga = models.IntegerField(default=0)
    points = models.IntegerField(default=0)
    home_played = models.IntegerField(default=0)
    away_played = models.IntegerField(default=0)

    class Meta:
        unique_together = ('league', 'team')
        ordering = ['-points', '-gf']
    
    @property
    def gd(self):
        """Різниця голів (Goal Difference)"""
        return self.gf - self.ga


class Odds(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name='odds')
    book = models.CharField(max_length=64)
    ts = models.DateTimeField()
    home_odds = models.FloatField()
    draw_odds = models.FloatField()
    away_odds = models.FloatField()

    class Meta:
        ordering = ['-ts']


class Event(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name='events')
    stat_name = models.CharField(max_length=64)
    value = models.FloatField()

    class Meta:
        indexes = [models.Index(fields=['stat_name'])]


class Player(models.Model):
    name = models.CharField(max_length=200)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='players')
    position = models.CharField(max_length=20, blank=True)

    class Meta:
        unique_together = ('name', 'team')
        ordering = ['name']

    def __str__(self) -> str:
        return f"{self.name}"


class Lineup(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name='lineups')
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='lineups')
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    is_starting = models.BooleanField(default=True)
    shirt_number = models.IntegerField(null=True, blank=True)

    class Meta:
        unique_together = ('match', 'player')
        ordering = ['team_id', '-is_starting', 'shirt_number']


class PlayerRating(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name='ratings')
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='ratings')
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    rating = models.FloatField()

    class Meta:
        unique_together = ('match', 'player')
        ordering = ['-rating']
