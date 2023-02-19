from django.urls import path
#from bookmark_collection import views

from . import views

urlpatterns = [
    path('add', views.add_entry),
    path('list', views.list_bookmark),
    path('add_m', views.add_entries),
    path('delete_e', views.delete_entry),
    path('update', views.update__d),
    path('get_slice', views.slice_),
    path('add_bl', views.add_bl),
]