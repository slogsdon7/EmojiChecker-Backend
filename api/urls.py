from django.contrib.auth import get_user_model
from django.urls import path, re_path, include
from djoser.views import UserViewSet
from rest_framework import routers
router = routers.DefaultRouter()
urlpatterns = router.urls

urlpatterns += [
    re_path(r'^auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
]
