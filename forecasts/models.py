from django.db import models
from django.utils import timezone
from core.models import Match


class Forecast(models.Model):
    match = models.OneToOneField(Match, on_delete=models.CASCADE, related_name='forecast')
    prob_home = models.FloatField()
    prob_draw = models.FloatField()
    prob_away = models.FloatField()
    confidence = models.CharField(max_length=10, choices=[('low', 'low'), ('medium', 'medium'), ('high', 'high')])
    explain = models.JSONField(default=list)
    recalculated_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-recalculated_at']

    def __str__(self) -> str:
        return f"Forecast for {self.match}"
