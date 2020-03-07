"""Urls"""
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('upload/', views.upload_file, name='upload'),
    path('<int:doc_id>/', views.document, name="document"),
]
