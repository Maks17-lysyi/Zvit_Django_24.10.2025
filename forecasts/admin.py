from django.contrib import admin
from .models import Forecast


@admin.register(Forecast)
class ForecastAdmin(admin.ModelAdmin):
    list_display = ('match', 'prob_home', 'prob_draw', 'prob_away', 'confidence', 'recalculated_at')
