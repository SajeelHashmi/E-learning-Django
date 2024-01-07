from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Student


class userSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email')


class studentSerializer(serializers.ModelSerializer):
    user = userSerializer(many=False, read_only=True)
    class Meta:
        model = Student
        fields = ('user', 'name', 'phoneNumber','id')

