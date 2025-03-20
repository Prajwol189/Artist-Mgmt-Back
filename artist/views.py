from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .db import get_db_connection

class ArtistSongsView(APIView):

    def get(self, request, artist_id=None):  # Ensure artist_id is passed to the method
        """Retrieve all songs of an artist"""
        if artist_id is None:
            return Response({"error": "Artist ID is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Query the database to get the songs for this artist
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM music WHERE artist_id = %s", (artist_id,))
        songs = cur.fetchall()
        cur.close()
        conn.close()

        return Response({"songs": songs}, status=status.HTTP_200_OK)

    def post(self, request):
        """Create a new song for an artist"""
        artist_id = request.data.get('artist_id')
        title = request.data.get('title')
        album_name = request.data.get('album_name')
        genre = request.data.get('genre')

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO music (artist_id, title, album_name, genre, created_at, updated_at) VALUES (%s, %s, %s, %s, NOW(), NOW()) RETURNING id",
            (artist_id, title, album_name, genre)
        )
        music_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()

        return Response({"message": "Song created successfully", "music_id": music_id}, status=status.HTTP_201_CREATED)

    def put(self, request, music_id):
        """Update a song (only by the artist who created it)"""
        artist_id = request.data.get('artist_id')
        title = request.data.get('title')
        album_name = request.data.get('album_name')
        genre = request.data.get('genre')

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "UPDATE music SET title = %s, album_name = %s, genre = %s, updated_at = NOW() WHERE id = %s AND artist_id = %s",
            (title, album_name, genre, music_id, artist_id)
        )
        conn.commit()
        cur.close()
        conn.close()

        return Response({"message": "Song updated successfully"}, status=status.HTTP_200_OK)

    def delete(self, request, music_id):
        """Delete a song (only by the artist who created it)"""
        artist_id = request.data.get('artist_id')

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM music WHERE id = %s AND artist_id = %s", (music_id, artist_id))
        conn.commit()
        cur.close()
        conn.close()

        return Response({"message": "Song deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
