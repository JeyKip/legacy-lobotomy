from rest_auth.views import UserDetailsView as RestAuthUserDetailsView
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.mixins import DestroyModelMixin
from rest_framework.permissions import IsAuthenticated

from .models import Team
from .permissions import IsNotSuperuser
from .serializers import (
    TeamDashboardSerializer
)


class UserDetailsView(DestroyModelMixin, RestAuthUserDetailsView):
    def get_permissions(self):
        if self.request.method.lower() == 'get':
            self.permission_classes = [IsAuthenticated]
        else:
            self.permission_classes = [IsAuthenticated, IsNotSuperuser]

        return super().get_permissions()

    def perform_update(self, serializer):
        serializer.save(first_login=False)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


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
