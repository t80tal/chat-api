from rest_framework import serializers

def full_name_validator(value):
    if len(value.split()) < 2:
        raise serializers.ValidationError("Plesae provide a valid full name.")
