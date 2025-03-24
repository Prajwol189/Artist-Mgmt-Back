from rest_framework import serializers
# Artist Serializer
class ArtistSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    dob = serializers.DateTimeField(required=False)
    gender = serializers.ChoiceField(choices=['m', 'g', 'o'])
    address = serializers.CharField(max_length=255, required=False)
    first_release_year = serializers.DateField(required=False)
    no_of_albums_released = serializers.IntegerField(required=False)

# Music Serializer
class MusicSerializer(serializers.Serializer):
    artist_id = serializers.IntegerField()
    title = serializers.CharField(max_length=255)
    album_id = serializers.IntegerField()  # Changed from album_name to album_id
    genre = serializers.ChoiceField(choices=['rnb', 'country', 'classic', 'rock', 'jazz'])













































































































































