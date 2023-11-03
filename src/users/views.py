from rest_auth.views import (
    LoginView as RALoginView
)
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import User, Team
from .permissions import IsNotSuperuser
from .serializers import (
    UserSerializer, TeamDashboardSerializer,
    LoginSerializer
)


class LoginView(RALoginView):
    serializer_class = LoginSerializer


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsNotSuperuser)

    def update(self, request, *args, **kwargs):
        data = request.data
        instance = self.get_object()
        if instance.first_login:
            data['first_login'] = False
        serializer = UserSerializer(instance, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class TeamDashboardViewSet(viewsets.ModelViewSet):
    serializer_class = TeamDashboardSerializer
    http_method_names = ['get']
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsNotSuperuser)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context

    def get_queryset(self):
        return Team.objects.filter(pk=self.request.user.team.id)

