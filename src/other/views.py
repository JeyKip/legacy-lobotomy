from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from users.permissions import IsNotSuperuser

from .models import TermsAndConditions
from .serializers import TermsAndConditionsSerializer


class TermsAndConditionsViewSet(viewsets.ModelViewSet):
    serializer_class = TermsAndConditionsSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsNotSuperuser)
    queryset = TermsAndConditions.objects.all()
    http_method_names = ['get', 'patch']

    def update(self, request, *args, **kwargs):
        user = request.user
        if not user.accepted_terms_cond:
            if request.data.get('accepted_terms_cond'):
                user.accepted_terms_cond = True
                user.save()

                return HttpResponse(
                    f'Terms and Condition is accepted for {request.user.email}',
                    status=200)
            return HttpResponse(
                'If you want to accept Terms and Conditions, '
                'add "accepted_terms_cond: true" to the body',
                status=400)
        return HttpResponse(
            'Terms and Conditions already accepted ',
            status=400)
