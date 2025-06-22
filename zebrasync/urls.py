from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # ─── Admin ────────────────────────────────────────────────
    path("admin/", admin.site.urls),

    # ─── Auth (django-allauth) ────────────────────────────────
    # включва login, logout, signup, Google OAuth, …
    path("accounts/", include("allauth.urls")),

    # ─── App routes ───────────────────────────────────────────
    # home, features, pricing, support, dashboard, uploads, …
    path("", include("core.urls")),
]

# ─── Static / Media in DEBUG (удобно при разработка) ─────────
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
