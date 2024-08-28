from rest_framework import serializers
from .models import UploadedImage,Person

class UploadedImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedImage
        fields = ('image', 'name', 'uploaded_at')

class ImageUploadSerializer(serializers.Serializer):
    image = serializers.ImageField()


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ['id', 'image', 'name', 'father_name', 'date_of_birth']
