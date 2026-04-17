from django.urls import path
from . import views


app_name = 'images'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:image_id>/', views.detail, name='detail'),
    path('<int:image_id>/delete/', views.delete, name='delete'),
    path('upload/', views.upload, name='upload'),
]
