from django.urls import (
    include,
    path,
    re_path
)

from rest_framework.routers import DefaultRouter

app_name = 'api'

router = DefaultRouter()

urlpatterns = [
    #path('', include('djoser.urls')),
    #path('auth/', include('djoser.urls.authtoken')),
    #url(r'^auth/', include('djoser.urls')),
    #path('auth/', include('djoser.urls')),
    #re_path(r'^auth/', include('djoser.urls.authtoken')),
    #re_path(r'^auth/', include('djoser.urls')),
    #re_path(r'^auth/', include('djoser.urls.authtoken')),
]
