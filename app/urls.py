from django.urls import path

from . import views


app_name = 'app'
urlpatterns = [
    path('create', views.combi_create, name='create'),
    path('list', views.combi_list, name='list'),
    path('detail/<int:pk>', views.combi_detail, name='detail'),
    path('delete/<int:pk>', views.combi_delete, name='delete'),
]
