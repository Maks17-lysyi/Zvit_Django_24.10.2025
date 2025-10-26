from django.urls import path
from . import views

urlpatterns = [
	path('', views.news_list, name='news_list'),
	path('tag/<str:tag_name>/', views.news_by_tag, name='news_by_tag'),
	path('<slug:slug>/', views.news_detail, name='news_detail'),
]
