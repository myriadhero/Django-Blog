from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "accounts"

    def ready(self) -> None:
        # Import signal handlers to ensure they are registered when the app is ready
        from . import signals  # noqa: F401
