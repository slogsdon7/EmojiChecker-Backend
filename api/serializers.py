from rest_framework import serializers
from api.models import Emoji, Schedule, Response, Message


class EmojiSerializer(serializers.ModelSerializer):

    class Meta:
        model = Emoji
        fields = ('name', 'description', 'emoji')


class ScheduleSerializer(serializers.ModelSerializer):
    message = serializers.RelatedField

    class Meta:
        model = Schedule
        fields = ('send_at', 'message', 'sent')

class ResponseSerializer(serializers.ModelSerializer):
    emoji = serializers.RelatedField
    user = serializers.RelatedField

    class Meta:
        model = Response
        fields = ('emoji', 'ts', 'user')
        read_only_fields = ('user',)


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('id', 'name', 'text')
