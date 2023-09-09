from django.contrib import admin

from .models import TermsAndConditions


@admin.register(TermsAndConditions)
class TermsAndConditionsAdmin(admin.ModelAdmin):

    def has_add_permission(self, request):
        return not TermsAndConditions.objects.exists()
