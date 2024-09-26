from django.apps import AppConfig


class RealTimeVoiceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'real_time_voice'

    def ready(self):
        from real_time_voice.signals import init_signals
        init_signals()
        return super(RealTimeVoiceConfig, self).ready()