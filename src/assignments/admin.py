from django.contrib import admin, messages
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.forms import BaseInlineFormSet
from django.http import HttpResponseRedirect
from django.urls import path
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from file_resubmit.admin import AdminResubmitMixin
from nested_inline.admin import NestedModelAdmin, NestedTabularInline

from .forms import AssignmentBlockForm, BulkUploadForm
from .models import (Assignment, Category, Option, TextBlock, ImageBlock,
                     VideoBlock, QuestionBlock, AssingmentTarget,
                     AssignmentBlock
                     )
from .utils import check_and_create_assignments, get_assignments_from_file, check_csv_file


def get_image_preview(obj, width=150, height=150):
    if obj.image:
        return mark_safe(
            '<img src="{0}" width="{1}" height="{2}" style="object-fit:contain" />'.format(
                obj.image.url, width, height))


def get_name_preview(obj):
    if obj.name:
        return mark_safe('<a href="../../../assignment/{0}/change/">{1}</a>'.format(obj.id, obj.name))

class AssignmentInline(admin.TabularInline):
    model = Assignment
    extra = 0

    fields = ['name_preview', 'points', 'image_preview']
    readonly_fields = ('image_preview', 'name_preview')

    def name_preview(self, obj):
        return get_name_preview(obj)

    def image_preview(self, obj):
        return get_image_preview(obj)

    def has_add_permission(self, request, obj):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    inlines = [
        AssignmentInline,
    ]


class TextInline(NestedTabularInline):
    model = TextBlock
    extra = 1


class ImageInLine(AdminResubmitMixin, NestedTabularInline):
    model = ImageBlock
    extra = 1


class VideoInLine(AdminResubmitMixin, NestedTabularInline):
    model = VideoBlock
    extra = 1


class OptionInlineFormset(BaseInlineFormSet):
    def clean(self):
        true_options_cnt = 0
        for form in self.forms:
            for field in form.changed_data:
                if field == 'is_correct' and form.cleaned_data['is_correct']:
                    true_options_cnt += 1
        if true_options_cnt > 1:
            raise ValidationError(
                "Only one correct answer per question"
            )


class OptionInLine(NestedTabularInline):
    model = Option
    extra = 1
    formset = OptionInlineFormset


class QuestionInline(NestedTabularInline):
    model = QuestionBlock
    extra = 1
    inlines = [OptionInLine]


class BlockInline(NestedTabularInline):
    model = AssignmentBlock
    extra = 1
    inlines = [
        TextInline,
        ImageInLine,
        VideoInLine,
        QuestionInline,
    ]

    form = AssignmentBlockForm

    class Media:
        js = (
            # '//ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js',
            'admin/js/base.js',
        )


@admin.register(Assignment)
class AssignmentAdmin(AdminResubmitMixin, NestedModelAdmin):
    readonly_fields = ['image_preview']
    search_fields = ('name',)
    ordering = ['priority']

    change_list_template = "admin/assignments_changelist.html"

    inlines = [
        BlockInline,
    ]

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('bulk_upload/', self.bulk_upload, name='bulk_upload'),
        ]
        return my_urls + urls

    urls = property(get_urls)

    def changelist_view(self, request, extra_context=None):
        view = super().changelist_view(request, extra_context)
        try:
            view.context_data['submit_csv_form'] = BulkUploadForm
        except Exception:
            return view
        return view

    def render_change_form(self, request, context, add=False, change=False,
                           form_url='', obj=None):
        if obj is not None:
            depend_on_ids = \
                Assignment.objects.filter(dependent_on=obj.id).values_list(
                    'id', flat=True)
            context['adminform'].form.fields['dependent_on'].queryset = \
                Assignment.objects.filter(~Q(id=obj.id) & ~Q(id__in=depend_on_ids))
        return super().render_change_form(request, context, add, change, form_url, obj)

    def image_preview(self, obj):
        return get_image_preview(obj)

    def bulk_upload(self, request):
        if request.method == 'POST':
            error = False
            error_message = None
            form = BulkUploadForm(request.POST, request.FILES)
            if form.is_valid():
                if len(form.files) > 0:
                    csv_file = form.files['csv_file']
                    error, error_message = check_csv_file(csv_file)
                    if not error:
                        assignments = get_assignments_from_file(csv_file)
                        error, error_message = check_and_create_assignments(assignments)
            else:
                error = True
                error_message = form.errors.get('csv_file').data[0].messages[0]
            if error:
                messages.error(request, error_message)
            else:
                messages.success(request, "Your assignments has been uploaded!")
        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)


@admin.register(AssingmentTarget)
class TargetAdmin(admin.ModelAdmin):
    fieldsets = (
        (_('Name'), {'fields': ('name',)}),
        (_('Age'), {'fields': ('min_age', 'max_age',)}),
        (_('Gender'),
         {'fields': (
             'male', 'female', 'non_binary', 'transgender', 'other',)}),
        (_('Activity'), {'fields': ('law_explorer',)}),
    )
    list_display = (
        'name', 'min_age', 'max_age', 'male', 'female', 'non_binary',
        'transgender', 'other', 'law_explorer',)
