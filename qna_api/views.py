import json

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated


from qna_api import serializers
from qna_api import models
from qna_api import permissions

import pusher

pusher_client = pusher.Pusher(
    app_id="1750303",
    key="b57ac495b11384ef6852",
    secret="04d6bd0362b12feaf762",
    cluster="ap2",
    ssl=True,
)


class UserProfileViewSet(viewsets.ModelViewSet):
    """Handle creating and updating profiles"""

    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnProfile,)

    @action(detail=False, methods=["get"], permission_classes=[IsAuthenticated])
    def me(self, request):
        """Return the profile of the logged in user"""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)


class UserLoginApiView(ObtainAuthToken):
    """Handle creating user authentication tokens"""

    # This is the default renderer for ObtainAuthToken
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class QuestionViewSet(viewsets.ModelViewSet):
    """Handle creating and updating questions"""

    serializer_class = serializers.QuestionSerializer
    queryset = models.Question.objects.all().order_by("-created_at")
    authentication_classes = (TokenAuthentication,)

    def perform_create(self, serializer):
        """Sets the user profile to the logged in user"""
        question = serializer.save(user=self.request.user)

        print(question)
        pusher_client.trigger(
            "my-channel",
            "my-event",
            {
                "question": json.dumps(
                    {
                        "id": question.id,
                        "title": question.title,
                        "text": question.text,
                        # "created_at": question.created_at,
                        "user": {
                            "id": question.user.id,
                            "avatar": QuestionViewSet.get_avatar_url(question.user),
                            "name": question.user.name,
                        },
                    }
                )
            },
        )

    def get_avatar_url(user):
        if user.avatar:
            return user.avatar.url
        else:
            return None
