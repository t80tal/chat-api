from rest_framework_simplejwt.authentication import JWTAuthentication

class Authentication(JWTAuthentication):
      
    def authenticate(self, request):
        token = request.COOKIES.get("Token") or None
        try:
            validated_token = self.get_validated_token(token.split(" ")[1])
            user = self.get_user(validated_token)
            user.password = None
            return user, validated_token
        except:
            return None
