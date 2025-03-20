from django.urls import path
from .views import ArtistSongsView

urlpatterns = [
    path('songs/', ArtistSongsView.as_view(), name='create_song'),
    path('songs/<int:artist_id>/', ArtistSongsView.as_view(), name='list_songs'),  # Ensure artist_id is in the URL
    path('songs/update/<int:music_id>/', ArtistSongsView.as_view(), name='update_song'),
    path('songs/delete/<int:music_id>/', ArtistSongsView.as_view(), name='delete_song'),
]
