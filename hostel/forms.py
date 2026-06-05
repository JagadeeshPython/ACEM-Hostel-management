from django import forms
from .models import LeaveRequest


class LeaveRequestForm(forms.ModelForm):

    class Meta:
        model = LeaveRequest

        fields = [
            'from_date',
            'to_date',
            'reason'
        ]

        widgets = {

            'from_date': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'form-control'
                }
            ),

            'to_date': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'form-control'
                }
            ),

            'reason': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 4,
                    'placeholder': 'Enter reason for leave'
                }
            ),
        }

    def clean(self):

        cleaned_data = super().clean()

        from_date = cleaned_data.get('from_date')
        to_date = cleaned_data.get('to_date')

        if from_date and to_date:

            if to_date < from_date:
                raise forms.ValidationError(
                    "To Date cannot be earlier than From Date."
                )

        return cleaned_data
    

from django import forms
from .models import Outpass


class OutpassForm(forms.ModelForm):

    class Meta:
        model = Outpass

        fields = [
            'destination',
            'reason',
            'out_time',
            'return_time',
            'emergency_contact'
        ]

        widgets = {
            'out_time': forms.DateTimeInput(
                attrs={'type': 'datetime-local'}
            ),

            'return_time': forms.DateTimeInput(
                attrs={'type': 'datetime-local'}
            ),
        }
        
from django import forms
from .models import Holiday

class HolidayForm(forms.ModelForm):
    class Meta:
        model = Holiday
        fields = '__all__'
        widgets = {
            'start_date': forms.DateInput(
                attrs={'type': 'date'}
            ),
            'end_date': forms.DateInput(
                attrs={'type': 'date'}
            ),
        }
        

from django import forms
from .models import Holiday

class HolidayForm(forms.ModelForm):
    class Meta:
        model = Holiday
        fields = '__all__'
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }