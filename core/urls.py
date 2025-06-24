from django.urls import path
from . import views

urlpatterns = [
    # ─── PUBLIC ROUTES ─────────────────────────
    path("", views.home, name="home"),
    path("features/", views.features_view, name="features"),
    path("pricing/", views.pricing_view, name="pricing"),
    path("support/", views.support_view, name="support"),

    # ─── AUTH ROUTES ───────────────────────────
    path("dashboard/", views.dashboard_view, name="dashboard"),
    path("upload/", views.upload_zip, name="upload_zip"),
    path("jobs/<int:job_id>/", views.job_detail, name="job_detail"),
    path("api/logs/<int:job_id>/", views.get_sync_logs, name="get_sync_logs"),
]
# test