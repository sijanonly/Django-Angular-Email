from rest_framework import serializers
from emailapp.models import (
    Message)

from django_angular_email.users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'middle_name', 'last_name', )


class MessageSerializer(serializers.ModelSerializer):

    sender = UserSerializer()

    class Meta:
        model = Message
        fields = (
            'id', 'sender', 'receivers', 'msg_header',
            'msg_content', 'created', 'is_opened')


class MessagePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
