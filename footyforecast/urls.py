"""
URL configuration for footyforecast project.

Це головний файл з URL маршрутами - він вказує які адреси ведуть до яких функцій.
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from forecasts import views as fviews
from django.http import HttpResponse
from django.urls import re_path



def robots_txt(request):
    """Файл robots.txt для пошукових систем (Google, Bing тощо)"""
    content = "User-agent: *\nDisallow:\n"
    return HttpResponse(content, content_type="text/plain")


def sitemap_xml(request):
    """Файл sitemap.xml для пошукових систем - карта сайту"""
    content = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"></urlset>
"""
    return HttpResponse(content, content_type="application/xml")



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
   
    re_path(r'^robots\.txt$', robots_txt),
    re_path(r'^sitemap\.xml$', sitemap_xml),
]
