from rest_framework import serializers

from .models import *

class PneumoniaSerializer(serializers.ModelSerializer):
    class Meta:
        model=Pneumonia
        fields='__all__'