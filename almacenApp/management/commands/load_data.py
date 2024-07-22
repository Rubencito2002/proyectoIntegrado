import requests
from django.core.management.base import BaseCommand
from almacenApp.models import Categoria, Marca, Producto
from django.core.files.base import ContentFile

class Command(BaseCommand):
    help = 'Load data from the Fake Store API'

    def handle(self, *args, **kwargs):
        url = 'https://fakestoreapi.com/products'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()

            # Definir las zonas del comercio
            zonas = {
                'electronics': 'Informática',
                'jewelery': 'Moda',
                'men\'s clothing': 'Moda',
                'women\'s clothing': 'Moda'
            }

            # Crear las categorías (zonas) si no existen
            for key, value in zonas.items():
                Categoria.objects.get_or_create(nombre=value)

            for item in data:
                # Obtener o crear la marca (categoria en la API)
                marca_name = item.get('category', 'Unknown')
                marca, _ = Marca.objects.get_or_create(nombre=marca_name.strip())

                # Determinar la zona (categoria en tu modelo)
                zona_name = zonas.get(marca_name, 'Zona General')
                categoria, _ = Categoria.objects.get_or_create(nombre=zona_name)

                # Crear o actualizar el producto
                producto, created = Producto.objects.get_or_create(
                    nombre=item['title'],
                    descripcion=item.get('description', ''),
                    precio=item.get('price', 0),
                    estado='disponible',
                    cantidad=item.get('stock', 100),
                    marca=marca,
                )

                # Descargar y guardar la imagen
                image_url = item.get('image')
                if image_url:
                    image_response = requests.get(image_url)
                    if image_response.status_code == 200:
                        img_temp = ContentFile(image_response.content)
                        producto.muestra.save(f"{producto.nombre}.jpg", img_temp, save=False)

                # Asignar la categoria (zona) al producto
                producto.categoria.add(categoria)
                
                producto.save()

            self.stdout.write(self.style.SUCCESS('Datos cargados exitosamente'))
        else:
            self.stdout.write(self.style.ERROR('Error al obtener datos de la API'))
