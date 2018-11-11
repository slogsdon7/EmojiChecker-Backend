from django.core.exceptions import ValidationError
from rest_framework import permissions
from rest_framework import viewsets, status
from rest_framework.response import Response as APIResponse

from api.models import Emoji, Message, Response, Schedule, SendLog
from api.serializers import EmojiSerializer, MessageSerializer, ResponseSerializer, ScheduleSerializer, \
    SendLogSerializer

# TODO: quick-fix for testing purposes. Turn into a config variable.
CHECK_SEND_LOG = True

class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_staff


class IsOwnerReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS and obj.user == request.user:
            return True
        return request.user.is_staff


class EmojiViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'put', 'delete']
    serializer_class = EmojiSerializer
    permission_classes = (IsAdminOrReadOnly,)
    queryset = Emoji.objects.all()


class MessageViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'put', 'delete']
    serializer_class = MessageSerializer
    permission_classes = (permissions.IsAdminUser,)
    queryset = Message.objects.all()


class ResponseViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'delete']
    serializer_class = ResponseSerializer
    permission_classes = (IsOwnerReadOnly, permissions.IsAuthenticated)
    filter_fields = ('user',)
    def get_queryset(self):
        if self.request.user.is_staff:
            return Response.objects.all()
        return Response.objects.filter(user=self.request.user)

    def create(self, request, format=None):
        """Respond to the most recent message. Returns 403 if user has already responded"""
        emoji, created = Emoji.objects.get_or_create(name=request.data['emoji'])
        response = Response(user=request.user, emoji=emoji)
        if not CHECK_SEND_LOG:
            response.save()
            SendLog.objects.create(response=response, user=request.user, success=True)
            api_response = APIResponse(data=ResponseSerializer(instance=response).data, status=status.HTTP_201_CREATED)
            return api_response
        try:
            sendlog = SendLog.objects.filter(success=True).filter(user=request.user).order_by('-ts')[0]
        except SendLog.DoesNotExist:
            return APIResponse(status=status.HTTP_503_SERVICE_UNAVAILABLE)

        if sendlog.response is None:
            sendlog.response = response
            try:
                response.save()
                sendlog.save()
            except ValidationError:
                return APIResponse(data={"Error": "Survey has expired"}, status=status.HTTP_403_FORBIDDEN)
            api_response = APIResponse(data=ResponseSerializer(instance=response).data, status=status.HTTP_201_CREATED)
        else:
            api_response = APIResponse(status=status.HTTP_503_SERVICE_UNAVAILABLE)
        return api_response


class ScheduleViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'put', 'delete']
    serializer_class = ScheduleSerializer
    permission_classes = (permissions.IsAdminUser,)
    queryset = Schedule.objects.all()


class SendLogViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (permissions.IsAdminUser,)
    serializer_class = SendLogSerializer
    queryset = SendLog.objects.all().order_by('-ts')
