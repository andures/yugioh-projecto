import requests
from django.core.management.base import BaseCommand
from yugioh_app.models import Carta

class Command(BaseCommand):
    help = 'Importa cartas desde la API de Yu-Gi-Oh! Pro'

    def handle(self, *args, **kwargs):
        # URL de la API de Yu-Gi-Oh! Pro
        api_url = 'https://db.ygoprodeck.com/api/v7/cardinfo.php'
        
        # Intentamos hacer una solicitud GET a la API sin parámetros (para obtener muchas cartas)
        try:
            response = requests.get(api_url)
            response.raise_for_status()  # Si la respuesta tiene error, lanzará una excepción

            # Extraemos los datos de las cartas de la respuesta JSON
            cartas_data = response.json().get('data', [])

            if not cartas_data:
                self.stdout.write(self.style.ERROR('No se encontraron cartas en la API.'))

            total_cartas = 0
            for carta_data in cartas_data:
                # Extraemos los datos de cada carta según la API
                nombre = carta_data.get('name', '')
                tipo = carta_data.get('type', '')
                nivel = carta_data.get('level', 0)
                ataque = carta_data.get('atk', 0)
                defensa = carta_data.get('def', 0)
                descripcion = carta_data.get('desc', '')
                imagen_url = carta_data.get('card_images', [{}])[0].get('image_url', '')

                # Atributos adicionales
                frame_type = carta_data.get('frameType', '')
                raza = carta_data.get('race', '')
                atributo = carta_data.get('attribute', '')

                # Si no hay valor para nivel, defensa o ataque, los establecemos en 0
                if nivel is None:
                    nivel = 0
                if defensa is None:
                    defensa = 0
                if ataque is None:
                    ataque = 0

                # Verificamos que todos los campos necesarios estén presentes
                if not nombre:
                    continue  # Si no tiene nombre, lo omitimos

                # Usamos update_or_create para evitar duplicados
                Carta.objects.update_or_create(
                    nombre=nombre,
                    defaults={
                        'tipo': tipo,
                        'nivel': nivel,
                        'ataque': ataque,
                        'defensa': defensa,
                        'descripcion': descripcion,
                        'imagen_url': imagen_url,
                        'frame_type': frame_type,
                        'raza': raza,
                        'atributo': atributo,
                    },
                )
                
                total_cartas += 1

            self.stdout.write(self.style.SUCCESS(f"Se han importado {total_cartas} cartas desde la API."))
        
        except requests.exceptions.RequestException as e:
            self.stdout.write(self.style.ERROR(f"Error al conectarse a la API: {e}"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Ocurrió un error: {str(e)}"))