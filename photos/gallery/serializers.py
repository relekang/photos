from rest_framework import serializers

from photos.gallery.models import Photo


class ThumbnailSerializer(serializers.Serializer):
    url = serializers.CharField()
    height = serializers.CharField()
    width = serializers.CharField()
    # ratio = serializers.FloatField()


class PhotoSerializer(serializers.ModelSerializer):
    large_thumbnail = ThumbnailSerializer(read_only=True)
    medium_thumbnail = ThumbnailSerializer(read_only=True)
    square_thumbnail = ThumbnailSerializer(read_only=True)

    class Meta:
        model = Photo
        fields = ('id', 'title', 'slug', 'large_thumbnail', 'medium_thumbnail', 'square_thumbnail')
