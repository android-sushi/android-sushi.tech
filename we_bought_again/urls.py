from django.urls import path

from . import views

app_name = 'we_bought_again'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
]