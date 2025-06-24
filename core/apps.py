from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        import os
        from django.conf import settings

        if settings.DEBUG:
            return  # локално работи – няма нужда

        try:
            from allauth.socialaccount.models import SocialApp
            from django.contrib.sites.models import Site
            from django.db.utils import OperationalError

            site = Site.objects.get_current()
            app, created = SocialApp.objects.get_or_create(
                provider="google",
                name="Google",
                defaults={
                    "client_id": os.environ.get("SOCIALACCOUNT_GOOGLE_CLIENT_ID"),
                    "secret": os.environ.get("SOCIALACCOUNT_GOOGLE_SECRET"),
                },
            )
            app.sites.add(site)
        except OperationalError:
            pass
        except Exception as e:
            print("⚠️ Could not configure SocialApp:", str(e))
