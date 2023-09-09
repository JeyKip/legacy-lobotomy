from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.contrib.auth.models import Group
from django.db.models import Q
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from rest_framework.authtoken.models import TokenProxy

from .forms import UserCreationForm
from .models import User, Team, UserProxy
from playbooks.models import PlaybookAssignment


def get_linked_name(obj, name_type):
    url = reverse(
        'admin:%s_%s_change' % (obj._meta.app_label,
                                obj._meta.model_name),
        args=[obj.id])
    if name_type == 'first_name':
        object_name = obj.first_name
    else:
        object_name = obj.last_name
    return format_html(
        '<a href="{0}">{1}</a>',
        url,
        object_name
    )


class UserInline(admin.TabularInline):
    model = User
    extra = 0

    fields = ['get_first_name', 'get_last_name', 'total_points']
    readonly_fields = ('get_first_name', 'get_last_name', 'total_points')

    @admin.display(description='First name')
    def get_first_name(self, obj):
        return get_linked_name(obj, 'first_name')

    @admin.display(description='Last name')
    def get_last_name(self, obj):
        return get_linked_name(obj, 'last_name')

    def has_add_permission(self, request, obj):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_queryset(self, request):
        return User.objects.filter(Q(is_superuser=False) &
                                   Q(first_login=False))\
            .order_by('-total_points', 'last_name')


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    # change_form_template = 'users/admin/change_form.html'
    fields = ['name', 'description', 'logo',
              'number_of_users', 'total_points']
    readonly_fields = ('number_of_users', 'total_points')
    inlines = [UserInline]

    def number_of_users(self, obj):
        return (User.objects.filter(Q(is_superuser=False) &
                                    Q(team_id=obj.id) &
                                    Q(first_login=False)))\
            .count()

    def total_points(self, obj):
        total_points = 0
        user_ids = []
        for user in User.objects.filter(Q(is_superuser=False) &
                                        Q(team_id=obj.id) &
                                        Q(first_login=False)):
            user_ids.append(user.id)
        for playbook_assignment in PlaybookAssignment.objects.filter(
                user_id__in=user_ids):
            total_points += playbook_assignment.points
        return total_points


class UserAdmin(DjangoUserAdmin):
    add_form = UserCreationForm
    delete_confirmation_template = 'users/admin/delete_confirmation.html'

    fieldsets = (
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email',
                                         'guardian_email', 'age', 'gender',
                                         'activity',
                                         'team')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        (_('Terms and Conditions'), {'fields': ('accepted_terms_cond',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'team',),
        }),
    )
    list_filter = tuple()
    list_display = ('email', 'get_first_name', 'get_last_name', 'guardian_email',
                    'age', 'gender', 'activity')
    ordering = ('email',)

    search_fields = ('email', 'first_name', 'last_name')

    def get_queryset(self, request):
        return User.objects.filter(is_superuser=False)

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['email', 'last_login', 'date_joined']
        return []

    @admin.display(description='First name')
    def get_first_name(self, obj):
        return get_linked_name(obj, 'first_name')

    @admin.display(description='Last name')
    def get_last_name(self, obj):
        return get_linked_name(obj, 'last_name')

    def get_deleted_objects(self, objs, request):
        """
        Allow deleting related objects if their model is present in admin_site
        and user does not have permissions to delete them from admin web
        """
        deleted_objects, model_count, perms_needed, protected = \
            super().get_deleted_objects(objs, request)
        return deleted_objects, model_count, set(), protected


class UserProxyAdmin(UserAdmin):
    list_display = ('email', 'get_first_name', 'get_last_name')

    fieldsets = (
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'is_superuser',),
        }),
    )

    def get_readonly_fields(self, request, obj=None):
        read_only_fields = ['is_superuser']
        if obj:
            read_only_fields += ['email', 'last_login', 'date_joined']
        return read_only_fields

    def get_queryset(self, request):
        return User.objects.filter(is_superuser=True)


admin.site.register(User, UserAdmin)
admin.site.register(UserProxy, UserProxyAdmin)

admin.site.unregister(Group)
admin.site.unregister(TokenProxy)
