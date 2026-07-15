
from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'users'

    def ready(self):
        # This registers the signals when Django starts up
        import users.signals