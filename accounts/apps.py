from django.apps import AppConfig


class AccountsConfig(AppConfig):
    name = "accounts"

    def ready(self):
        import accounts.signals  # noqa (Pylint error from Django 4.0 ahead versions)
