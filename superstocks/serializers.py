from rest_framework import serializers
from .models import SuperStokist


class SuperstockistSerializer(serializers.ModelSerializer):
    class Meta:
        model = SuperStokist
        fields = ('__all__')