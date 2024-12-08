# retail/forms.py
from django import forms
from .models import Wholesale
from datetime import datetime, date


class RetailForm(forms.ModelForm):

    class Meta:
        model = Wholesale
        fields = '__all__'
        widgets = {
            'order_date': forms.DateInput(attrs={
                'type': 'date',
                'max': datetime.now().date(),
                'min': date(2020, 1, 1)
            })
        }
        input_formats = ['%d.%m.%Y']