from rest_framework import serializers

from chat.models import Mssg

class MssgSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mssg
        fields = ["text",  ]

class MssgDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mssg
        fields = ["id", "text", "user" , "key_to_recepient"]
