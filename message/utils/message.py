from message.models import Message
from user.models import AuthUser
from django.db.models import Q
from typing import Literal


def has_permission_for_message(message_id: int, user: AuthUser, level: Literal["both", "receiver", "sender"]):
    message = Message.objects.filter(Q(sender=user.id) & Q(id=message_id))
    if level == "receiver":
        message = Message.objects.filter(Q(receiver=user.id) & Q(id=message_id))
    if level == "both":
        message = Message.objects.filter((Q(sender=user.id) | Q(receiver=user.id)) & Q(id=message_id))
    if not message and not user.is_superuser:
        return False
    return True
