import os
from django.db import migrations

def create_google_socialapp(apps, schema_editor):
    SocialApp = apps.get_model("socialaccount", "SocialApp")
    Site = apps.get_model("sites", "Site")

    site = Site.objects.get(id=1)

    app = SocialApp.objects.create(
        provider="google",
        name="Google",
        client_id=os.environ["SOCIALACCOUNT_GOOGLE_CLIENT_ID"],
        secret=os.environ["SOCIALACCOUNT_GOOGLE_SECRET"],
    )
    app.sites.add(site)

class Migration(migrations.Migration):
    dependencies = [
        ('core', '0001_initial'),
        ('sites', '0002_alter_domain_unique'),
        ('socialaccount', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_google_socialapp),
    ]
