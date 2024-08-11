from rest_framework import serializers
from .models import MatchRecord

class MatchRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = MatchRecord
        fields = '__all__'