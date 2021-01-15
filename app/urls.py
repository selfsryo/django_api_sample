from django.urls import path

from . import views


app_name = 'apps'
urlpatterns = [
    path('create', views.combi_create, name='combi_create'),
    path('list', views.combi_list, name='combi_list'),
    path('detail/<int:pk>', views.combi_detail, name='combi_detail'),
    path('delete/<int:pk>', views.combi_delete, name='combi_delete'),
]
