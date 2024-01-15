from rest_framework import serializers
from .models import Note
from django.contrib.auth.models import User


class NoteAPISerializer(serializers.ModelSerializer):

    class Meta:
        model = Note
        fields = ['pk', 'title', 'text']


class RegisterAPISerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'confirm_password']

    extra_kwargs = {
        'password': {'write_only': True},
    }

    def validate(self, data):
        password = data.get('password')
        confirm_password = data.get('confirm_password')

        if password != confirm_password:
            raise serializers.ValidationError("Passwords do not match.")

        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password', None)
        user = User.objects.create_user(**validated_data)
        return {'id': user.id, 'username': user.username, 'password': None}


class LoginAPISerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password']


class UserProfileAPISerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
