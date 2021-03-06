from . models import User, Video, Rating
from rest_framework import serializers
from rest_framework.authtoken.models import Token

class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = "__all__"

        extra_kwargs = {"url": {"required": True}}


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ("id", "stars", "user", "video", "comments")


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "password")

        extra_kwargs = {"password": {"required": True, "write_only": True}}

        def create(self, validated_data):
            user = User.objects.create_user(**validated_data)
            Token.objects.create(user=user)
            return user
