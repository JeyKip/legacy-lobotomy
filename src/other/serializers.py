from rest_framework import serializers

from .models import TermsAndConditions


class TermsAndConditionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TermsAndConditions
        fields = '__all__'
