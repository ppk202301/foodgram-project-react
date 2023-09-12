from django.urls import (
    include,
    path,
    re_path
)

from rest_framework.routers import DefaultRouter


router = DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')), 
    path('auth/', include('djoser.urls.authtoken')),
]
