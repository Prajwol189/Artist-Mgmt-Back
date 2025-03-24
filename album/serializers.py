from rest_framework import serializers
from datetime import datetime

class AlbumSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=255)
    release_date = serializers.DateField()

    # Optional: You can add custom validation methods
    def validate_name(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("Album name must be at least 3 characters long.")
        return value



def validate_release_date(self, value):
    # Convert the string to a datetime.date object
    future_date = datetime.strptime("2025-01-01", "%Y-%m-%d").date()
    
    if value > future_date:  # Compare dates
        raise serializers.ValidationError("Release date cannot be in the future.")
    return value
