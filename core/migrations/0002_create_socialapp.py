import os
from django.db import migrations


def create_google_socialapp(apps, schema_editor):
    Site = apps.get_model("sites", "Site")
    SocialApp = apps.get_model("socialaccount", "SocialApp")

    site, _ = Site.objects.get_or_create(
        id=1,
        defaults={
            "domain": "zebrasync.onrender.com",
            "name": "ZebraSync",
        },
    )

    app, _ = SocialApp.objects.get_or_create(
        provider="google",
        name="Google",
        client_id=os.environ.get("SOCIALACCOUNT_GOOGLE_CLIENT_ID"),
        secret=os.environ.get("SOCIALACCOUNT_GOOGLE_SECRET"),
    )

    app.sites.add(site)


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0001_initial"),  # Името на твоята последна миграция
        ("sites", "0002_alter_domain_unique"),
        ("socialaccount", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(create_google_socialapp),
    ]
