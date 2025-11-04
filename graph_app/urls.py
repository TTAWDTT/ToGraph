from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('convert/', views.convert, name='convert'),
    path('view/<str:file_id>/', views.view_graph, name='view_graph'),
    path('download/<str:file_id>/', views.download_graph, name='download_graph'),
]
