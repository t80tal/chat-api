from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from user.models import AuthUser


def response_with_token(user: AuthUser, response_data):
    access_token = str(RefreshToken.for_user(user).access_token)
    response = Response(response_data)
    response.set_cookie("Token", f"Bearer {access_token}")
    return response
