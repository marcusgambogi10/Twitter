from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"

        def update(self, validated_data):
            profile = ProfileSerializer()
            self.bio = validated_data.get("bio", self.bio)
            profile.save()
            return profile


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(required=False)

    class Meta:
        model = get_user_model()
        fields = "__all__"

    def create(self, validated_data):
        profile_data = validated_data.pop("profile", {})
        user = get_user_model().objects.create(**validated_data)
        Profile.objects.create(user=user, **profile_data)
        return user
