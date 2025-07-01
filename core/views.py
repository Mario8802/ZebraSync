from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import SyncJob, LogLine
from .forms import ZipUploadForm
from .tasks import run_sync
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from allauth.socialaccount.models import SocialApp
from django.contrib.sites.models import Site

# core/views.py
from django.http import JsonResponse
from allauth.socialaccount.models import SocialApp
from django.contrib.sites.models import Site


from allauth.socialaccount.models import SocialApp
from django.contrib.sites.models import Site
from django.conf import settings
from django.contrib.sites.models import Site
from django.http import HttpResponse

def init_site(request):
    site, created = Site.objects.get_or_create(
        id=1,
        defaults={"domain": "zebrasync.onrender.com", "name": "ZebraSync"}
    )
    if not created:
        site.domain = "zebrasync.onrender.com"
        site.name = "ZebraSync"
        site.save()
        return HttpResponse("✅ Site updated.")
    return HttpResponse("✅ Site created.")
def init_socialapp(request):
    site = Site.objects.get_current()

    if not SocialApp.objects.filter(provider="google").exists():
        app = SocialApp.objects.create(
            provider="google",
            name="Google",
            client_id=settings.SOCIALACCOUNT_GOOGLE_CLIENT_ID,
            secret=settings.SOCIALACCOUNT_GOOGLE_SECRET,
        )
        app.sites.add(site)
        return HttpResponse("✅ Google SocialApp created.")
    return HttpResponse("ℹ️ SocialApp already exists.")

def debug_socialapp(request):
    try:
        app = SocialApp.objects.filter(provider="google").first()
        site = Site.objects.get_current()
        return JsonResponse({
            "social_app_found": bool(app),
            "client_id": app.client_id if app else None,
            "secret": app.secret[:5] + "..." if app and app.secret else None,
            "linked_sites": [s.domain for s in app.sites.all()] if app else [],
            "current_site": site.domain,
            "site_id": site.id
        })
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

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
