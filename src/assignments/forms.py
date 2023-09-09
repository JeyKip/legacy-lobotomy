from django import forms
from assignments.models import AssignmentBlock


class AssignmentBlockForm(forms.ModelForm):
    class Meta:
        model = AssignmentBlock
        fields = ('type_of_block', )
        widgets = {
            'type_of_block': forms.Select(choices=AssignmentBlock.TYPE_CHOICES)
        }


class BulkUploadForm(forms.Form):
    csv_file = forms.FileField(label="Please select a csv file",
                               widget=forms.FileInput(
                                   attrs={'accept': '.csv'}))
