from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from qna_api import serializers
from qna_api import models
from qna_api import permissions


class UserProfileViewSet(viewsets.ModelViewSet):
    """Handle creating and updating profiles"""

    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnProfile,)


class UserLoginApiView(ObtainAuthToken):
    """Handle creating user authentication tokens"""

    # This is the default renderer for ObtainAuthToken
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class QuestionViewSet(viewsets.ModelViewSet):
    """Handle creating and updating questions"""

    serializer_class = serializers.QuestionSerializer
    queryset = models.Question.objects.all()
    authentication_classes = (TokenAuthentication,)

    def perform_create(self, serializer):
        """Sets the user profile to the logged in user"""
        serializer.save(user=self.request.user)
