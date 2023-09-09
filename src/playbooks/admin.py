from django.contrib import admin
from django.db.models import Q
from django.urls import reverse
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from nested_inline.admin import NestedModelAdmin, NestedTabularInline

from users.models import User

from .models import (PlaybookAssignment, PlaybookTextBlock, PlaybookImageBlock,
                     PlaybookVideoBlock, PlaybookOption,
                     PlaybookQuestionBlock, PlaybookAssignmentBlock
                     )


def get_image_preview(obj, width=150, height=150):
    if obj.image:
        return mark_safe(
            '<img src="{0}" width="{1}" height="{2}" style="object-fit:contain" />'.format(
                obj.image.url, width, height))


class PlaybookTextInline(NestedTabularInline):
    model = PlaybookTextBlock

    fields = ('text',)
    readonly_fields = ['text']

    def has_delete_permission(self, request, obj=None):
        return False


class PlaybookImageInLine(NestedTabularInline):
    model = PlaybookImageBlock

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj):
        return False


class PlaybookVideoInLine(NestedTabularInline):
    model = PlaybookVideoBlock

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj):
        return False


class PlaybookOptionInLine(NestedTabularInline):
    model = PlaybookOption

    fields = ('text', 'tip')
    readonly_fields = ['text', 'tip', 'is_correct']
    fieldsets = (
        (None, {
            'fields': (
                'text', 'tip', 'is_correct'
            )
        }),
    )

    def has_add_permission(self, request, obj):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class PlaybookQuestionInline(NestedTabularInline):
    model = PlaybookQuestionBlock
    inlines = [PlaybookOptionInLine]

    fields = ('text',)
    readonly_fields = ['text']

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj):
        return False


class PlaybookBlockInline(NestedTabularInline):
    model = PlaybookAssignmentBlock
    inlines = [
        PlaybookTextInline,
        PlaybookImageInLine,
        PlaybookVideoInLine,
        PlaybookQuestionInline,
    ]

    fields = ('type_of_block',)
    readonly_fields = ['type_of_block']

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj):
        return False


@admin.register(PlaybookAssignment)
class PlaybookAssignmentAdmin(NestedModelAdmin):
    readonly_fields = ['user', 'name', 'image', 'image_preview', 'description',
                       'points', 'time', 'category', 'priority', 'dependent_on']
    inlines = [
        PlaybookBlockInline,
    ]

    change_form_template = 'admin/playbook/change_list.html'

    def image_preview(self, obj):
        return get_image_preview(obj)

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def render_change_form(self, request, context, add=False, change=False,
                           form_url='', obj=None):
        context.update({
            'show_save': False,
            'show_save_and_continue': False
        })
        return super().render_change_form(request, context, add, change,
                                          form_url, obj)


class UserPlaybookInline(NestedTabularInline):
    model = PlaybookAssignment
    extra = 0
    max_num = 0

    ordering = ('-completed',)

    fieldsets = (
        (None, {
            'fields': (
                'assignment', 'description', 'points', 'time',
                'priority'
            )
        }),
    )
    readonly_fields = ['assignment', 'description', 'points', 'time',
                       'priority']

    def assignment(self, obj):
        url = reverse(
                    'admin:%s_%s_change' % (obj._meta.app_label,
                                            obj._meta.model_name),
                    args=[obj.id])
        return format_html(
            '<a href="{0}">{1}</a>',
            url,
            obj
        )

    def has_delete_permission(self, request, obj=None):
        return False


class UsersPlaybook(User):
    class Meta:
        proxy = True


class UserPlaybookAdmin(admin.ModelAdmin):
    list_display = ('email',)
    fieldsets = (
        (None, {'fields': ('email',)}),
        (None, {'fields': ('points',)}),
    )

    inlines = [
        UserPlaybookInline
    ]

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['email', 'points']
        return []

    def get_queryset(self, request):
        return User.objects.filter(is_superuser=False).order_by('last_name')

    def points(self, obj):
        total_points = 0
        for assignment in PlaybookAssignment.objects.filter(user_id=obj.id):
            total_points += assignment.points
        return total_points

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False

    def render_change_form(self, request, context, add=False, change=False,
                           form_url='', obj=None):
        context.update({
            'show_save': False,
            'show_save_and_continue': False
        })
        return super().render_change_form(request, context, add, change,
                                          form_url, obj)


admin.site.register(UsersPlaybook, UserPlaybookAdmin)
