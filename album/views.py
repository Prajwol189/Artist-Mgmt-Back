from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import connection
from .serializers import AlbumSerializer

class AlbumView(APIView):
    def get(self, request):
        with connection.cursor() as cursor:
            # Update the SQL query to include artist_id
            cursor.execute("""
                SELECT album.id, album.name, album.release_date, album.artist_id
                FROM album
            """)
            columns = [col[0] for col in cursor.description]
            albums = [dict(zip(columns, row)) for row in cursor.fetchall()]

        # Use the serializer to format the output
        serializer = AlbumSerializer(albums, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = AlbumSerializer(data=request.data)
        if serializer.is_valid():
            name = serializer.validated_data['name']
            release_date = serializer.validated_data['release_date']

            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO album (name, release_date)
                    VALUES (%s, %s) RETURNING id
                """, [name, release_date])
                album_id = cursor.fetchone()[0]

            return Response({"message": "Album created", "id": album_id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, album_id):
        serializer = AlbumSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            release_date = serializer.validated_data.get('release_date')

            with connection.cursor() as cursor:
                cursor.execute("""
                    UPDATE album
                    SET name = %s, release_date = %s, updated_at = CURRENT_TIMESTAMP
                    WHERE id = %s
                """, [name, release_date, album_id])

            return Response({"message": "Album updated"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, album_id):
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM album WHERE id = %s", [album_id])

        return Response({"message": "Album deleted"}, status=status.HTTP_204_NO_CONTENT)
