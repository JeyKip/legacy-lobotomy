from django.db.models import Q
from rest_auth.models import TokenModel
from rest_auth.serializers import (
    PasswordResetSerializer as RAPasswordResetSerializer,
    PasswordResetConfirmSerializer as RAPasswordResetConfirmSerializer,
    LoginSerializer as RALoginSerializer
)
from rest_framework import serializers

from .models import User, Team


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'pk',
            'email',
            'first_name',
            'last_name',
            'age',
            'gender',
            'guardian_email',
            'accepted_terms_cond',
            'activity',
            'total_points',
            'first_login',
            'is_superuser'
        )



class UserMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('pk', 'email', 'first_login', 'accepted_terms_cond')


class TokenSerializer(serializers.ModelSerializer):
    user = UserMiniSerializer(many=False)

    class Meta:
        model = TokenModel
        fields = ('key', 'user')


class LoginSerializer(RALoginSerializer):
    password = serializers.CharField(style={'input_type': 'password'},
                                     trim_whitespace=False)


class PasswordResetSerializer(RAPasswordResetSerializer):
    def get_email_options(self):
        return {
            'html_email_template_name': 'registration/email_password_reset_confirm.html',
            'subject_template_name': 'registration/password_reset_subject.txt'
        }

    def validate_email(self, value):
        self.reset_form = self.password_reset_form_class(data=self.initial_data)
        if not self.reset_form.is_valid() and 'email' in self.reset_form.errors:
            raise serializers.ValidationError(self.reset_form.errors['email'])

        return value


class PasswordResetConfirmSerializer(RAPasswordResetConfirmSerializer):
    new_password1 = serializers.CharField(max_length=128, trim_whitespace=False)
    new_password2 = serializers.CharField(max_length=128, trim_whitespace=False)


class TeamDashboardUserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    rank = serializers.SerializerMethodField()
    rank_var = 0

    class Meta:
        model = User
        fields = ('rank', 'name', 'total_points')

    def get_name(self, obj):
        request = self.context.get('request')
        if request.user.id == obj.id:
            return 'You'
        return '{0} {1}'.format(obj.last_name, obj.first_name)

    def get_rank(self, obj):
        self.rank_var += 1
        return self.rank_var


class TeamDashboardSerializer(serializers.ModelSerializer):
    users = serializers.SerializerMethodField()

    class Meta:
        model = Team
        fields = ('name', 'description', 'logo', 'users')

    def get_users(self, obj):
        return TeamDashboardUserSerializer(
            User.objects.filter(Q(team_id=obj.id) &
                                Q(first_login=False) &
                                Q(is_superuser=False))
                .order_by('-total_points', 'last_name'),
            many=True, context=self.context).data
