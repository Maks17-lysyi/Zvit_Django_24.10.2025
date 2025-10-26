from django.db import models


# ===== МОДЕЛІ ДЛЯ ЛІГ ТА КОМАНД =====

class League(models.Model):
    """Модель футбольної ліги (наприклад, Ла Ліга, Прем'єр Ліга)"""
    
    code = models.CharField(max_length=50)  # Код ліги
    name = models.CharField(max_length=200)  # Назва ліги
    country = models.CharField(max_length=100, blank=True)  # Країна
    is_active = models.BooleanField(default=True)  # Чи активна ліга

    class Meta:
        # Не може бути двох ліг з однаковим кодом та назвою
        unique_together = ('code', 'name')
        # Сортуємо за країною та назвою
        ordering = ['country', 'name']

    def __str__(self):
        return self.name


class Team(models.Model):
    """Модель футбольної команди"""
    
    name = models.CharField(max_length=200)  # Назва команди
    league = models.ForeignKey(League, on_delete=models.CASCADE, related_name='teams')  # До якої ліги належить

    class Meta:
        # Не може бути двох команд з однаковою назвою в одній лізі
        unique_together = ('name', 'league')
        # Сортуємо за назвою
        ordering = ['name']

    def __str__(self):
        return self.name


# ===== МОДЕЛІ ДЛЯ МАТЧІВ =====

class Match(models.Model):
    """Модель футбольного матчу"""
    
    match_id = models.CharField(max_length=64, unique=True)  # Унікальний ID матчу
    season = models.CharField(max_length=20)  # Сезон (наприклад, 2024/2025)
    league = models.ForeignKey(League, on_delete=models.CASCADE, related_name='matches')  # В якій лізі
    date_utc = models.DateTimeField()  # Дата та час матчу
    round = models.CharField(max_length=50, blank=True)  # Раунд/тур
    stadium = models.CharField(max_length=200, blank=True)  # Стадіон
    home_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='home_matches')  # Команда-господар
    away_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='away_matches')  # Команда-гість
    is_published = models.BooleanField(default=True)  # Чи опублікований матч

    class Meta:
        # Індекси для швидкого пошуку
        indexes = [
            models.Index(fields=['date_utc']),
            models.Index(fields=['league', 'season']),
        ]
        # Сортуємо за датою
        ordering = ['date_utc']

    def __str__(self):
        return f"{self.home_team} vs {self.away_team} ({self.date_utc.date()})"


class Result(models.Model):
    """Результат матчу"""
    
    match = models.OneToOneField(Match, on_delete=models.CASCADE, related_name='result')  # Зв'язок з матчем
    home_goals = models.IntegerField()  # Голи господарів
    away_goals = models.IntegerField()  # Голи гостей
    status = models.CharField(max_length=20, choices=[
        ('finished', 'Завершено'),
        ('postponed', 'Відкладено')
    ])  # Статус матчу

    def __str__(self):
        return f"{self.match}: {self.home_goals}-{self.away_goals}"


# ===== ТУРНІРНА ТАБЛИЦЯ =====

class Standing(models.Model):
    """Турнірна таблиця - статистика команди в лізі"""
    
    league = models.ForeignKey(League, on_delete=models.CASCADE, related_name='standings')  # Ліга
    team = models.ForeignKey(Team, on_delete=models.CASCADE)  # Команда
    played = models.IntegerField(default=0)  # Зіграно матчів
    won = models.IntegerField(default=0)  # Перемог
    draw = models.IntegerField(default=0)  # Нічиїх
    lost = models.IntegerField(default=0)  # Поразок
    gf = models.IntegerField(default=0)  # Забито голів (Goals For)
    ga = models.IntegerField(default=0)  # Пропущено голів (Goals Against)
    points = models.IntegerField(default=0)  # Очки (3 за перемогу, 1 за нічию)
    home_played = models.IntegerField(default=0)  # Матчів вдома
    away_played = models.IntegerField(default=0)  # Матчів в гостях

    class Meta:
        # Одна команда може бути тільки один раз в таблиці кожної ліги
        unique_together = ('league', 'team')
        # Сортуємо за очками, потім за забитими голами
        ordering = ['-points', '-gf']
    
    @property
    def gd(self):
        """Різниця голів (Goal Difference)"""
        return self.gf - self.ga


# ===== КОЕФІЦІЄНТИ ТА ПОДІЇ =====

class Odds(models.Model):
    """Коефіцієнти букмекерів на матч"""
    
    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name='odds')  # Матч
    book = models.CharField(max_length=64)  # Назва букмекера
    ts = models.DateTimeField()  # Час запису коефіцієнтів
    home_odds = models.FloatField()  # Коефіцієнт на перемогу господарів
    draw_odds = models.FloatField()  # Коефіцієнт на нічию
    away_odds = models.FloatField()  # Коефіцієнт на перемогу гостей

    class Meta:
        ordering = ['-ts']  # Сортуємо від новіших до старіших


class Event(models.Model):
    """Події матчу (статистика)"""
    
    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name='events')  # Матч
    stat_name = models.CharField(max_length=64)  # Назва статистики (удари, пас, тощо)
    value = models.FloatField()  # Значення

    class Meta:
        indexes = [models.Index(fields=['stat_name'])]  # Індекс для швидкого пошуку


# ===== ГРАВЦІ =====

class Player(models.Model):
    """Футбольний гравець"""
    
    name = models.CharField(max_length=200)  # Ім'я гравця
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='players')  # Команда
    position = models.CharField(max_length=20, blank=True)  # Позиція (захисник, нападник, тощо)

    class Meta:
        # Гравець з таким ім'ям може бути тільки один в команді
        unique_together = ('name', 'team')
        ordering = ['name']

    def __str__(self):
        return self.name


class Lineup(models.Model):
    """Склад команди на матч"""
    
    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name='lineups')  # Матч
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='lineups')  # Гравець
    team = models.ForeignKey(Team, on_delete=models.CASCADE)  # Команда
    is_starting = models.BooleanField(default=True)  # Чи грає з першої хвилини
    shirt_number = models.IntegerField(null=True, blank=True)  # Номер на футболці

    class Meta:
        # Гравець може бути тільки один раз в складі на матч
        unique_together = ('match', 'player')
        # Спочатку основний склад, потім запасні
        ordering = ['team_id', '-is_starting', 'shirt_number']


class PlayerRating(models.Model):
    """Рейтинг гравця в матчі"""
    
    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name='ratings')  # Матч
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='ratings')  # Гравець
    team = models.ForeignKey(Team, on_delete=models.CASCADE)  # Команда
    rating = models.FloatField()  # Оцінка (наприклад, від 0 до 10)

    class Meta:
        # Гравець може мати тільки один рейтинг за матч
        unique_together = ('match', 'player')
        # Сортуємо від вищого до нижчого
        ordering = ['-rating']
