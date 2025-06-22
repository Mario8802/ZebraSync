from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import SyncJob, LogLine
from .forms import ZipUploadForm
from .tasks import run_sync
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def get_sync_logs(request, job_id):
    logs = LogLine.objects.filter(job_id=job_id).order_by("ts")
    data = [{"level": log.level, "message": log.message} for log in logs]
    return JsonResponse(data, safe=False)


# ──────────────────────────  PUBLIC PAGES  ──────────────────────────
def home(request):
    return render(request, "home.html")


def features_view(request):
    return render(request, "features.html")


def pricing_view(request):
    return render(request, "pricing.html")


def support_view(request):
    return render(request, "support.html")


# ─────────────────────  AUTHENTICATED / DASHBOARD  ───────────────────
@login_required
def dashboard_view(request):
    """Landing page after login – shows upload + recent jobs."""
    sync_jobs = (
        SyncJob.objects
        .filter(user=request.user)
        .order_by("-created_at")
    )
    return render(request, "dashboard.html", {"sync_jobs": sync_jobs})


@login_required
def upload_zip(request):
    """Handle ZIP upload + trigger Celery sync task."""
    if request.method == "POST":
        form = ZipUploadForm(request.POST, request.FILES)
        if form.is_valid():
            job = SyncJob.objects.create(
                user=request.user,
                src_zip=form.cleaned_data["src_zip"]
            )
            run_sync.delay(job.id)
            return redirect("job_detail", job_id=job.id)
    else:
        form = ZipUploadForm()

    return render(request, "core/upload.html", {"form": form})


@login_required
def job_detail(request, job_id):
    """Show log lines for a specific sync job."""
    job = get_object_or_404(SyncJob, id=job_id, user=request.user)
    logs = job.logs.all().order_by("ts")
    return render(request, "core/job_detail.html", {"job": job, "logs": logs})
