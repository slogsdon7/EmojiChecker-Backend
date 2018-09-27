from rest_framework import viewsets
from rest_framework.reverse import reverse
from api.serializers import EmojiSerializer, MessageSerializer, ResponseSerializer, ScheduleSerializer
from api.models import Emoji, Message, Response, Schedule
from django.dispatch import receiver
from rest_framework import permissions


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
    serializer_class = EmojiSerializer
    permission_classes = (IsAdminOrReadOnly,)
    queryset = Emoji.objects.all()


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = (permissions.IsAdminUser,)
    queryset = Message.objects.all()


class ResponseViewSet(viewsets.ModelViewSet):
    serializer_class = ResponseSerializer
    permission_classes = (IsOwnerReadOnly,)
    queryset = Response.objects.all()

    def create(self, request):
        """TODO: Validate message to ensure it isn't a duplicate"""
        pass


class ScheduleViewSet(viewsets.ModelViewSet):
    serializer_class = ScheduleSerializer
    permission_classes = (permissions.IsAdminUser,)
    queryset = Schedule.objects.all()

