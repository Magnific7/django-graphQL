from django.forms import ModelForm
from .models import ReconModel

class ExcelForm(ModelForm):
    class Meta: 
        model = ReconModel
        fields = '__all__'
