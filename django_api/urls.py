from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/combi/', include('app.urls')),
    path('api/token/', include('api_token.urls')),
]
