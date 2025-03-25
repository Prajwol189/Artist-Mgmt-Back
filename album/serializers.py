from rest_framework import serializers

class AlbumSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=255)
    release_date = serializers.DateField()
    artist_id = serializers.IntegerField()  # Include artist_id here

    def validate_name(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("Album name must be at least 3 characters long.")
        return value

    def validate_release_date(self, value):
        future_date = datetime.strptime("2025-01-01", "%Y-%m-%d").date()
        if value > future_date:
            raise serializers.ValidationError("Release date cannot be in the future.")
        return value
