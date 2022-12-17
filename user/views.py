from user.utils.token import response_with_token
from user.serializers.user import UserSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from user.models import AuthUser


@api_view(["POST"])
def register(request):
    serialized = UserSerializer(data=request.data)
    if not serialized.is_valid():
        return Response(serialized.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    user = serialized.save()

    return response_with_token(user, serialized.data)


@api_view(["POST"])
def login(request):
    if not "username" in request.data or not "password" in request.data:
        return Response({"message": "Username and password are required fields."}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    username = request.data["username"]
    password = request.data["password"]
    user = AuthUser.objects.filter(Q(username=username)).first()

    if not user or not user.check_password(password):
        return Response({"message": "Invalid username or password."}, status=status.HTTP_401_UNAUTHORIZED)

    return response_with_token(user, UserSerializer(user).data)


@api_view(["POST"])
def logout(request):
    response = Response({"message": "Successfully logged out."})
    response.delete_cookie("Token")
    return response
