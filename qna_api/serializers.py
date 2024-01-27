from rest_framework import serializers

from qna_api import models


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializes a user profile object"""

    class Meta:
        model = models.UserProfile
        fields = ("id", "email", "name", "password", "avatar")
        extra_kwargs = {
            "password": {"write_only": True, "style": {"input_type": "password"}},
            "avatar": {"required": False},
        }

    def create(self, validated_data: dict):
        """Create and return a new user"""

        user = models.UserProfile(
            email=validated_data["email"],
            name=validated_data["name"],
            avatar=validated_data.get("avatar", None),
        )

        user.set_password(validated_data["password"])
        user.save()

        return user

    def update(self, instance: models.UserProfile, validated_data: dict):
        """Handle updating user account"""
        if "password" in validated_data:
            password = validated_data.pop("password")
            instance.set_password(password)

        avatar = validated_data.pop("avatar", None)
        if avatar:
            instance.avatar = avatar

        return super().update(instance, validated_data)


class QuestionSerializer(serializers.ModelSerializer):
    """Serializes a question object"""

    user = UserProfileSerializer(read_only=True)

    class Meta:
        model = models.Question
        fields = ("id", "user", "title", "text", "created_at")
        extra_kwargs = {
            "user": {"read_only": True},
            "created_at": {"read_only": True},
            "id": {"read_only": True},
            "updated_at": {"read_only": True},
        }

    def create(self, validated_data):
        """Create and return a new question"""

        question = models.Question(
            title=validated_data["title"],
            text=validated_data["text"],
            user=self.context["request"].user,
        )

        question.save()

        return question
