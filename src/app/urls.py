from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from users.views import UserDetailsView, TeamDashboardViewSet
from other.views import TermsAndConditionsViewSet

from assignments.apiviews import (
    AssingmentViewSet,
    UserDiscoverViewSet,
    UserPlaybookViewSet,
    CategoryViewSet
)

router = DefaultRouter()
router.register('team-dashboard', TeamDashboardViewSet, 'Team Dashboard')
router.register('terms-conditions', TermsAndConditionsViewSet, 'Terms and Conditions')
router.register('assignments', AssingmentViewSet)
router.register('categories', CategoryViewSet)
router.register('discover', UserDiscoverViewSet, basename='Discover')
router.register('playbook', UserPlaybookViewSet, basename='Playbook')

urlpatterns = [
    path(
        'password-reset-confirm/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(),
        name='password_reset_confirm'
    ),
    path('reset_done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('auth/user/', UserDetailsView.as_view()),
    path('auth/', include('rest_auth.urls')),
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]

urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
