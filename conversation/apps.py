from django.apps import AppConfig


class ConversationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'conversation'

    def ready(self):
        from conversation.signals import init_signals
        init_signals()
        return super(ConversationConfig, self).ready()