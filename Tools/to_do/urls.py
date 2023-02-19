from django.urls import path

from . import views

urlpatterns = [
    path('list', views.list_to_do),
    path('add', views.add_to_do),
    path('delete', views.delete_todo),
]