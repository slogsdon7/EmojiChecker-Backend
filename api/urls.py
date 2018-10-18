from django.urls import re_path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import routers, permissions

from api.views import EmojiViewSet, MessageViewSet, ResponseViewSet, ScheduleViewSet, SendLogViewSet

schema_view = get_schema_view(
   openapi.Info(
      title="Emoji-Backend API",
      default_version='v1',
      description="Work in progress.",
   ),
   validators=['flex', 'ssv'],
   public=True,
   permission_classes=(permissions.AllowAny,),
)

router = routers.DefaultRouter()
router.register('emoji',EmojiViewSet)
router.register('messages',MessageViewSet)
router.register('responses', ResponseViewSet, base_name='responses')
router.register('schedule', ScheduleViewSet)
router.register('sendlog', SendLogViewSet)


urlpatterns = router.urls
urlpatterns += [
    re_path(r'^auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
