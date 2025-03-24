from .serializers import ArtistSerializer,MusicSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import connection
from django.urls import path

# Artist Views
class ArtistView(APIView):
    def get(self, request):
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM artist")
            columns = [col[0] for col in cursor.description]
            artists = [dict(zip(columns, row)) for row in cursor.fetchall()]
        return Response(artists, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ArtistSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO artist (name, dob, gender, address, first_release_year, no_of_albums_released)
                    VALUES (%s, %s, %s, %s, %s, %s) RETURNING id
                """, [data['name'], data.get('dob'), data['gender'], data.get('address'), data.get('first_release_year'), data.get('no_of_albums_released')])
                artist_id = cursor.fetchone()[0]
            return Response({"message": "Artist created", "id": artist_id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, artist_id):
        serializer = ArtistSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            data = serializer.validated_data
            update_fields = ", ".join([f"{key} = %s" for key in data.keys()])
            values = list(data.values()) + [artist_id]
            with connection.cursor() as cursor:
                cursor.execute(f"UPDATE artist SET {update_fields}, updated_at = CURRENT_TIMESTAMP WHERE id = %s", values)
            return Response({"message": "Artist updated"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, artist_id):
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM artist WHERE id = %s", [artist_id])
        return Response({"message": "Artist deleted"}, status=status.HTTP_204_NO_CONTENT)

# Music Views
class MusicView(APIView):
    def get(self, request):
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM music")
            columns = [col[0] for col in cursor.description]
            music_list = [dict(zip(columns, row)) for row in cursor.fetchall()]
        return Response(music_list, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = MusicSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO music (artist_id, title, album_id, genre)
                    VALUES (%s, %s, %s, %s) RETURNING id
                """, [data['artist_id'], data['title'], data['album_id'], data['genre']])
                music_id = cursor.fetchone()[0]
            return Response({"message": "Music created", "id": music_id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, music_id):
        serializer = MusicSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            data = serializer.validated_data
            update_fields = ", ".join([f"{key} = %s" for key in data.keys()])
            values = list(data.values()) + [music_id]
            with connection.cursor() as cursor:
                cursor.execute(f"UPDATE music SET {update_fields}, updated_at = CURRENT_TIMESTAMP WHERE id = %s", values)
            return Response({"message": "Music updated"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, music_id):
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM music WHERE id = %s", [music_id])
        return Response({"message": "Music deleted"}, status=status.HTTP_204_NO_CONTENT)