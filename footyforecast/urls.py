"""
URL configuration for footyforecast project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from forecasts import views as fviews
from django.http import HttpResponse
from django.urls import re_path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', fviews.home, name='home'),
    path('matches/', fviews.matches_list, name='matches_list'),
    path('tables/', fviews.tables_view, name='tables'),
    path('analytics/', fviews.analytics_view, name='analytics'),
    path('contacts/', fviews.contacts_view, name='contacts'),
    path('league/<int:league_id>/', fviews.league_detail, name='league_detail'),
    path('team/<int:team_id>/', fviews.team_detail, name='team_detail'),
    path('match/<int:match_id>/', fviews.match_detail, name='match_detail'),
    path('news/', include('news.urls')),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='docs'),
    re_path(r'^robots\.txt$', lambda r: HttpResponse("User-agent: *\nDisallow:\n", content_type="text/plain")),
    re_path(r'^sitemap\.xml$', lambda r: HttpResponse("""<?xml version=\"1.0\" encoding=\"UTF-8\"?>
<urlset xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\"></urlset>
""", content_type="application/xml")),
]
