from django.apps import AppConfig


class PrezolaConfig(AppConfig):
    name = 'prezola'

    def ready(self):
        import prezola.signals
