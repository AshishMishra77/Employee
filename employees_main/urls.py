from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views
from accounts import views as AccountsViews

urlpatterns = [
    path("admin/", admin.site.urls),

    # Home
    path("", views.home, name="home"),

    # Employee app
    path("employee/", include("employees.urls")),

    # Auth (accounts app)
    path("register/", AccountsViews.register, name="register"),
    path("login/", AccountsViews.login_view, name="login"),
    path("logout/", AccountsViews.logout_view, name="logout"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
