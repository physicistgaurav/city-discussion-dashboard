from django.urls import path 
from app import views

urlpatterns = [
    path('health',views.health_check, name="health-check"),
    path('fetch-news/', views.fetch_news, name='fetch_news'),
    path('fetch-comments/', views.fetch_comments, name='fetch_comments'),
]
