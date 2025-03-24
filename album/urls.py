from django.urls import path
from .views import AlbumView

urlpatterns = [
    path('albums/', AlbumView.as_view(), name='album-list'),
    path('albums/<int:album_id>/', AlbumView.as_view(), name='album-detail'),
]
