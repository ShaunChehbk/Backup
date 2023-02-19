from django.urls import path

from . import views

urlpatterns = [
    path('touch', views.touch),
    path('list', views.list_words),
    path('random', views.get_sample),
    path('random_untouched', views.get_untouched),
    path('add_int', views.add_int),
]