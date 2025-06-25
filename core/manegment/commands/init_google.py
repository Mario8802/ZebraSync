from django.core.management.base import BaseCommand
from allauth.socialaccount.models import SocialApp
from django.contrib.sites.models import Site
import os

class Command(BaseCommand):
    help = "Creates the Google SocialApp for Django Allauth"

    def handle(self, *args, **options):
        site, _ = Site.objects.get_or_create(
            id=1,
            defaults={
                "domain": "zebrasync.onrender.com",
                "name": "ZebraSync"
            }
        )

        app, created = SocialApp.objects.get_or_create(
            provider="google",
            defaults={
                "name": "Google",
                "client_id": os.environ.get("SOCIALACCOUNT_GOOGLE_CLIENT_ID"),
                "secret": os.environ.get("SOCIALACCOUNT_GOOGLE_SECRET"),
            }
        )

        app.sites.set([site])
        self.stdout.write("✅ Google SocialApp initialized successfully.")
