from django.db import models
from django.conf import settings
# Create your models here.
class SyncJob(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    src_zip = models.FileField(upload_to="uploads/")
    status = models.CharField(max_length=20, default="queued")
    created_at = models.DateTimeField(auto_now_add=True)

class LogLine(models.Model):
    job = models.ForeignKey(SyncJob, on_delete=models.CASCADE, related_name="logs")
    ts = models.DateTimeField(auto_now_add=True)
    level = models.CharField(max_length=8)
    message = models.TextField()
#TEST 1