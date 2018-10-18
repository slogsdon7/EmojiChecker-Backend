from rest_framework import serializers

from api.models import Emoji, Schedule, Response, Message


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('id', 'name', 'text')


class EmojiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Emoji
        fields = ('name', 'description', 'emoji')


class ScheduleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Schedule
        fields = ('send_at', 'message', 'sent')
        read_only_fields = ('sent',)


class ScheduleListSerializer(ScheduleSerializer):
    message = MessageSerializer


class ResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Response
        fields = ('emoji', 'ts', 'user')
        read_only_fields = ('user',)


