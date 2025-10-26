from django.db import models
from django.utils import timezone
from core.models import Match


class Forecast(models.Model):
    """Прогноз на футбольний матч"""
    
    match = models.OneToOneField(Match, on_delete=models.CASCADE, related_name='forecast')
    
    # Ймовірності результатів (від 0.0 до 1.0)
    prob_home = models.FloatField()  # Ймовірність перемоги господарів
    prob_draw = models.FloatField()  # Ймовірність нічиї
    prob_away = models.FloatField()  # Ймовірність перемоги гостей
    
    # Рівень впевненості
    confidence = models.CharField(max_length=10, choices=[
        ('low', 'Низька'),
        ('medium', 'Середня'),
        ('high', 'Висока')
    ])
    
    # Пояснення прогнозу (JSON список - детальні фактори)
    explain = models.JSONField(default=list, blank=True)
    
    # Коли був розрахований прогноз
    recalculated_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-recalculated_at']

    def __str__(self):
        return f"Прогноз на {self.match}"
