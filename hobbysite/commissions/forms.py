from django import forms
from .models import Commission, Job

class CommissionForm(forms.ModelForm):
    class Meta:
        model = Commission
        exclude = ['created_on', 'updated_on', 'author']

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['status', 'commission', 'role', 'manpower_required']
