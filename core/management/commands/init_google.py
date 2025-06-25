from django.core.management.base import BaseCommand
from allauth.socialaccount.models import SocialApp
from django.contrib.sites.models import Site
from django.conf import settings

class Command(BaseCommand):
    help = "Create Google OAuth App and attach it to current Site"

    def handle(self, *args, **kwargs):
        site = Site.objects.get(id=settings.SITE_ID)
        app, _ = SocialApp.objects.update_or_create(
            provider="google",
            defaults={
                "name": "Google",
                "client_id": settings.SOCIALACCOUNT_GOOGLE_CLIENT_ID,
                "secret": settings.SOCIALACCOUNT_GOOGLE_SECRET,
            },
        )
        app.sites.set([site])
        self.stdout.write(self.style.SUCCESS(" Google OAuth setup complete"))
