from django.core.management.base import BaseCommand
from core.models import Match
from forecasts.services import compute_forecast


class Command(BaseCommand):
    help = 'Recompute forecasts for all matches (or a single match)'

    def add_arguments(self, parser):
        parser.add_argument('--match_id', type=str)

    def handle(self, *args, **options):
        qs = Match.objects.all()
        if options.get('match_id'):
            qs = qs.filter(match_id=options['match_id'])
        count = 0
        for m in qs:
            compute_forecast(m)
            count += 1
        self.stdout.write(self.style.SUCCESS(f'Recomputed {count} forecasts'))

