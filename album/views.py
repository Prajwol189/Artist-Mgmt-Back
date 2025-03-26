from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import connection
from .serializers import AlbumSerializer

class AlbumView(APIView):
    def get(self, request):
        with connection.cursor() as cursor:
            # Fetch albums with artist names using INNER JOIN
            cursor.execute("""
                SELECT album.id, album.name, album.release_date, 
                       album.artist_id, artist.name AS artist_name
                FROM album
                INNER JOIN artist ON album.artist_id = artist.id
            """)
            columns = [col[0] for col in cursor.description]
            albums = [dict(zip(columns, row)) for row in cursor.fetchall()]

        return Response(albums, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = AlbumSerializer(data=request.data)
        if serializer.is_valid():
            name = serializer.validated_data['name']
            release_date = serializer.validated_data['release_date']
            artist_id = serializer.validated_data['artist_id']

            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO album (name, release_date, artist_id)
                    VALUES (%s, %s, %s) RETURNING id
                """, [name, release_date, artist_id])
                album_id = cursor.fetchone()[0]

            return Response({"message": "Album created", "id": album_id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, album_id):
        serializer = AlbumSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            release_date = serializer.validated_data.get('release_date')
            artist_id = serializer.validated_data.get('artist_id')

            with connection.cursor() as cursor:
                cursor.execute("""
                    UPDATE album
                    SET name = %s, release_date = %s, artist_id = %s, updated_at = CURRENT_TIMESTAMP
                    WHERE id = %s
                """, [name, release_date, artist_id, album_id])

            return Response({"message": "Album updated"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, album_id):
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM album WHERE id = %s", [album_id])

        return Response({"message": "Album deleted"}, status=status.HTTP_204_NO_CONTENT)
