from django.apps import AppConfig


class TiendaappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tiendaApp'

    def ready(self):
        import tiendaApp.signals
