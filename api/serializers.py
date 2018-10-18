from rest_framework import serializers

from api.models import Emoji, Schedule, Response, Message, SendLog, User


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('id', 'name', 'text')


class EmojiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Emoji
        fields = ('name', 'description', 'emoji')



class ScheduleSerializer(serializers.ModelSerializer):
    users = serializers.PrimaryKeyRelatedField(many=True, read_only=False, queryset=User.objects.all())
    class Meta:
        model = Schedule
        fields = ('send_at', 'message', 'sent', 'users')
        read_only_fields = ('sent',)


class ScheduleListSerializer(ScheduleSerializer):
    message = MessageSerializer

    class Meta:
        model = Schedule
        fields = ('__all__',)


class ResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Response
        fields = ('emoji', 'ts', 'user')
        read_only_fields = ('user',)


class SendLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = SendLog
        fields = '__all__'
