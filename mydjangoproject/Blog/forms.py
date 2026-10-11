from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError

from .models import Mark, Student, Subject


class StaffAuthenticationForm(AuthenticationForm):
    def confirm_login_allowed(self, user):
        super().confirm_login_allowed(user)
        if not user.is_staff:
            raise ValidationError('This account is not allowed to access the staff dashboard.', code='not_staff')


class BootstrapModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault('class', 'form-control')


class StudentForm(BootstrapModelForm):
    class Meta:
        model = Student
        fields = ['student_number', 'first_name', 'last_name', 'class_name', 'email']
        labels = {'class_name': 'Class'}


class SubjectForm(BootstrapModelForm):
    class Meta:
        model = Subject
        fields = ['code', 'name']


class MarkForm(BootstrapModelForm):
    class Meta:
        model = Mark
        fields = ['student', 'subject', 'assessment', 'score', 'out_of']
        labels = {'assessment': 'Assessment or term', 'score': 'Mark earned', 'out_of': 'Maximum mark'}
        widgets = {
            'student': forms.Select(attrs={'class': 'form-control select2'}),
            'subject': forms.Select(attrs={'class': 'form-control select2'}),
            'score': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'step': '0.01'}),
            'out_of': forms.NumberInput(attrs={'class': 'form-control', 'min': '0.01', 'step': '0.01'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        score = cleaned_data.get('score')
        out_of = cleaned_data.get('out_of')
        if score is not None and out_of is not None and score > out_of:
            self.add_error('score', 'The mark cannot be greater than the maximum mark.')
        return cleaned_data
