from django.urls import path
from .views import ArtistView, MusicView

# URL Routing
urlpatterns = [
    path('artists/', ArtistView.as_view(), name='artist-list'),
    path('artists/<int:artist_id>/', ArtistView.as_view(), name='artist-detail'),
    path('music/', MusicView.as_view(), name='music-list'),
    path('music/<int:music_id>/', MusicView.as_view(), name='music-detail'),
]
