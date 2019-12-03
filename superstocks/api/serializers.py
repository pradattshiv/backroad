from rest_framework import serializers

from superstocks.models import Retailer

class RetailerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Retailer
        fields = ('__all__')
        

class loginSerializer(serializers.ModelSerializer):
    # username = serializers.CharField()
    # email = serializers.CharField()
    # password = serializers.CharField(style={'input_type':'password'},write_only= True)

    class Meta:
        model = Retailer
        fields = ('__all__')