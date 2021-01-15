from django.urls import path

from . import views


app_name = 'api_token'
urlpatterns = [
    path('create', views.token_create, name='token_create'),
]
