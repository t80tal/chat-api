from rest_framework.decorators import permission_classes, api_view
from message.utils.message import has_permission_for_message
from message.serializers.message import MessageSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from message.models import Message
from django.db.models import Q


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_message(request):
    serialized = MessageSerializer(
        data={"sender": request.user.username, **request.data})
    if not serialized.is_valid():
        return Response(serialized.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    serialized.save()
    return Response(serialized.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_messages(request):
    messages = Message.objects.filter(
        Q(sender=request.user.id) | Q(receiver=request.user.id)).all()
    messages = list(messages.values("id", "sender", "receiver",
                    "message", "subject", "has_read", "creation_date"))
    return Response(messages)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_undread_messages(request):
    messages = Message.objects.filter(
        Q(receiver=request.user.id) & Q(has_read=False)).all()
    messages = list(messages.values("id", "sender", "receiver",
                    "message", "subject", "has_read", "creation_date"))
    return Response(messages)


@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def read_message(request, message_id):
    message = Message.objects.filter(id=message_id)
    if not message:
        return Response({"message": f"Message: {message_id} does not exist"}, status=status.HTTP_404_NOT_FOUND)

    if not has_permission_for_message(message_id, request.user, level="receiver"):
        return Response({"message": f"Not allowed to read message: {message_id}."}, status=status.HTTP_403_FORBIDDEN)

    message.update(has_read=True)
    message = message.values("id", "sender", "receiver",
                             "message", "subject", "has_read", "creation_date")

    return Response(message)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_message(request, message_id):
    message = Message.objects.filter(id=message_id)
    if not message:
        return Response({"message": f"Message: {message_id} does not exist"}, status=status.HTTP_404_NOT_FOUND)

    if not has_permission_for_message(message_id, request.user, level="both"):
        return Response({"message": f"Not allowed to delete message: {message_id}."}, status=status.HTTP_403_FORBIDDEN)

    message.delete()

    return Response({"message": f"Deleted message: {message_id} successfully."})
