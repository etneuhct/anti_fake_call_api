from django.apps import AppConfig


class ThirdPartiesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'third_parties'

    def ready(self):
        from third_parties.signals import init_signals
        init_signals()
        return super(ThirdPartiesConfig, self).ready()