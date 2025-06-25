import os
from django.core.management.base import BaseCommand
from allauth.socialaccount.models import SocialApp
from django.contrib.sites.models import Site

class Command(BaseCommand):
    help = "Create Google OAuth SocialApp and link it to the current site"

    def handle(self, *args, **kwargs):
        site = Site.objects.get_current()

        client_id = os.getenv("SOCIALACCOUNT_GOOGLE_CLIENT_ID")
        secret = os.getenv("SOCIALACCOUNT_GOOGLE_SECRET")

        if not client_id or not secret:
            self.stderr.write(self.style.ERROR("Missing Google client ID or secret in environment."))
            return

        app, created = SocialApp.objects.update_or_create(
            provider="google",
            defaults={
                "name": "Google",
                "client_id": client_id,
                "secret": secret,
            },
        )

        app.sites.set([site])

        if created:
            self.stdout.write(self.style.SUCCESS("✅ Google SocialApp created and linked to site."))
        else:
            self.stdout.write(self.style.SUCCESS("🔄 Google SocialApp updated and re-linked to site."))
