from rest_framework import serializers
from .models import UploadedImage

class UploadedImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedImage
        fields = ('image', 'name', 'uploaded_at')

class ImageUploadSerializer(serializers.Serializer):
    image = serializers.ImageField()