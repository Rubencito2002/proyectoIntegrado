import requests
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from almacenApp.models import Categoria, Marca, Producto

class Command(BaseCommand):
    help = 'Load data from the Open Food Facts API into the database'

    def handle(self, *args, **kwargs):
        # URL de la API de Open Food Facts
        url = 'https://world.openfoodfacts.org/cgi/search.pl'
        params = {
            'search_terms': '',
            'search_simple': 1,
            'action': 'process',
            'json': 1,
            'page_size': 100
        }

        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            self.load_food_data(data)
            self.stdout.write(self.style.SUCCESS('Datos de alimentación cargados exitosamente'))
        else:
            self.stdout.write(self.style.ERROR('Error al obtener datos de la API de Open Food Facts'))

    def load_food_data(self, data):
        zona_name = 'Supermercado'
        categoria, _ = Categoria.objects.get_or_create(nombre=zona_name)

        for item in data.get('products', []):
            marca_name = item.get('brands', 'Unknown')
            marca, _ = Marca.objects.get_or_create(nombre=marca_name.strip())

            # Asignar un precio predeterminado si no está disponible en la API
            precio = item.get('price') if 'price' in item else 0.0  # Puedes establecer un valor predeterminado aquí

            producto, created = Producto.objects.get_or_create(
                nombre=item.get('product_name', 'Unknown'),
                descripcion=item.get('ingredients_text', ''),
                precio=precio,
                estado='disponible',
                cantidad=100,  # Puedes ajustar esto según sea necesario
                marca=marca,
            )

            image_url = item.get('image_url')
            if image_url:
                image_response = requests.get(image_url)
                if image_response.status_code == 200:
                    img_temp = ContentFile(image_response.content)
                    producto.muestra.save(f"{producto.nombre}.jpg", img_temp, save=False)

            producto.save()

            producto.categoria.add(categoria)
            producto.save()
