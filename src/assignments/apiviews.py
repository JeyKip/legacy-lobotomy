from datetime import date

from rest_framework.viewsets import ModelViewSet
from django.http import HttpResponse

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from .models import Assignment, UserAssignment, Category
from playbooks.models import PlaybookAssignment
from .serializers import (
    AssingmentSerializer, UserPlaybookSerializer, CategorySerializer)
from playbooks.utils import create_playbook_assignment
from users.models import User
from users.permissions import IsNotSuperuser


class AssingmentViewSet(ModelViewSet):
    queryset = Assignment.objects.all()
    serializer_class = AssingmentSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsNotSuperuser)


class UserDiscoverViewSet(ModelViewSet):
    serializer_class = AssingmentSerializer

    def get_queryset(self):
        queryset = Assignment.objects.filter(
            userassignment__user=self.request.user.id,
            userassignment__is_completed=False
        )
        ids = []
        for item in queryset:
            ids.append(item.id)

        queryset = Assignment.objects.filter(id__in=ids).order_by('priority')[:4]
        return queryset

    def update(self, request, *args, **kwargs):
        if request.data.get('is_completed'):
            userassignment = UserAssignment.objects.get(
                assignment=kwargs['pk'], user=request.user.id)
            userassignment.is_completed = True
            userassignment.completed = date.today()
            userassignment.save()

            assignment = Assignment.objects.get(pk=kwargs['pk'])

            create_playbook_assignment(user=request.user,
                                        assignment=assignment)

            return HttpResponse(
                f'Assignment "{userassignment.assignment.name}" marked '
                f'as completed for {request.user.email}',
                status=200, )
        return HttpResponse(
            'If you want to set assignment as complete, '
            'add "is_complete: true" to the body',
            status=400)


class UserPlaybookViewSet(ModelViewSet):
    serializer_class = UserPlaybookSerializer
    http_method_names = ['get']
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsNotSuperuser)

    def get_queryset(self):
        return User.objects.filter(pk=self.request.user.id)


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsNotSuperuser)
    http_method_names = ['get']
