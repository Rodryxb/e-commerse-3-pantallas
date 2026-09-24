import requests
from django.core.management.base import BaseCommand
from store.models import AtpRanking

class Command(BaseCommand):
    help = 'Importa el Top 10 ATP desde Matchstat (RapidAPI)'

    def handle(self, *args, **options):
        url = "https://site.api.espn.com/apis/site/v2/sports/tennis/atp/rankings"
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            # Borrar ranking viejo
            AtpRanking.objects.all().delete()
            
            # Extraer top 10 desde ESPN
            ranks = data.get('rankings', [])[0].get('ranks', [])[:10]
            
            for item in ranks:
                AtpRanking.objects.create(
                    rank=item.get('current', 0),
                    player_name=item['athlete']['displayName'],
                    country=item['athlete'].get('citizenshipCountry', 'UNK'),
                    points=int(item.get('points', 0))
                )
            self.stdout.write(self.style.SUCCESS('Ranking ATP sincronizado correctamente desde ESPN.'))
        except requests.exceptions.RequestException as e:
            self.stderr.write(f"Error de conexión con la API: {e}. Se mantienen los datos anteriores por seguridad.")
