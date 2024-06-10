"""blogsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from blog.sitemaps import CategorySitemap, PostSitemap
from ckeditor_uploader import views as ckeditor_views
from core.views import AboutPageView, healthcheck_view
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path, re_path

sitemaps = {
    "categories": CategorySitemap,
    "posts": PostSitemap,
}

urlpatterns = [
    path(settings.ADMIN_PATH, admin.site.urls),
    path("", include("blog.urls", namespace="blog")),
    path("about/", AboutPageView.as_view(), name="about"),
    path("feedback", include("feedback.urls", namespace="feedback")),
    path("healthcheck/", healthcheck_view, name="healthcheck"),
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),
    re_path(r"^ckeditor/upload/", ckeditor_views.upload, name="ckeditor_upload"),
    path("ckeditor/", include("ckeditor_uploader.urls")),
    path("select2/", include("django_select2.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns.append(path("__debug__/", include("debug_toolbar.urls")))
