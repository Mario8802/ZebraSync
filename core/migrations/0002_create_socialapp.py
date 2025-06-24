import os

from django.contrib.sites.models import Site

def create_google_socialapp(apps, schema_editor):
    Site = apps.get_model("sites", "Site")
    SocialApp = apps.get_model("socialaccount", "SocialApp")


    site, _ = Site.objects.get_or_create(
        id=1,
        defaults={
            "domain": "zebrasync.onrender.com",
            "name":   "ZebraSync",
        },
    )

    app, _ = SocialApp.objects.get_or_create(
        provider="google",
        name="Google",
        client_id=os.environ.get("SOCIALACCOUNT_GOOGLE_CLIENT_ID"),
        secret=os.environ.get("SOCIALACCOUNT_GOOGLE_SECRET"),
    )

    app.sites.add(site)
