from rest_framework import serializers
from message.models import Message
from user.models import AuthUser


class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.SlugRelatedField(many=False, slug_field="username", queryset=AuthUser.objects.all())
    receiver = serializers.SlugRelatedField(many=False, slug_field="username", queryset=AuthUser.objects.all())
    message = serializers.CharField(min_length=6, write_only=True)
    subject = serializers.CharField(min_length=6, write_only=True)
    # Auto created:
    id = serializers.IntegerField(required=False, read_only=True)
    has_read = serializers.BooleanField(required=False, read_only=True)
    creation_date = serializers.DateTimeField(required=False, read_only=True)

    class Meta:
        model = Message
        fields = ["id", "sender", "receiver", "message", "subject", "has_read", "creation_date"]
