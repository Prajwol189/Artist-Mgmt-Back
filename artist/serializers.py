from rest_framework import serializers

class ArtistSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=255)
    dob = serializers.DateTimeField()
    gender = serializers.ChoiceField(choices=['m', 'g', 'o'])
    address = serializers.CharField(max_length=255)
    first_release_year = serializers.DateField()
    no_of_albums_released = serializers.IntegerField()
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
