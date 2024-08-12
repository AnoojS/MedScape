from django.forms import ModelForm
from .models import *

class PneumoniaFormForm(ModelForm):
    class Meta:
        model=Pneumonia
        fields='__all__'