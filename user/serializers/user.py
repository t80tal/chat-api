from rest_framework.validators import UniqueValidator
from user.validators.user import full_name_validator
from rest_framework import serializers
from user.models import AuthUser

class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(min_length=6, validators=[UniqueValidator(queryset=AuthUser.objects.all())])
    password = serializers.CharField(min_length=6, write_only=True)
    full_name = serializers.CharField(min_length=4, validators=[full_name_validator])
    email = serializers.EmailField(validators=[UniqueValidator(queryset=AuthUser.objects.all())])
    # Auto created:
    id = serializers.IntegerField(required=False, read_only=True)

    class Meta:
        model = AuthUser
        fields = ["id", "username", "password", "full_name", "email"]
