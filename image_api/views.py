import os
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import UploadedImage
from .serializers import UploadedImageSerializer,ImageUploadSerializer
#from .enroll import Enrollment_Face
from django.conf import settings
from PIL import Image, ImageFilter
from django.http import HttpResponse
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import numpy as np

class ImageUploadView(APIView):
    def post(self, request):
        serializer = UploadedImageSerializer(data=request.data)
        print('data', request.data)
        if serializer.is_valid():
            print('The if statemtent hit...')
            serializer.save()
            image_instance = serializer.instance
            print('serializer:',serializer )
            print('image_instance', image_instance )
            
            # Rename the folder with the name provided by the user
            new_folder_name = image_instance.name
            #print('path of the folder', new_folder_name )
            new_folder_path = os.path.join(settings.MEDIA_ROOT, 'uploads', new_folder_name)
            #print('path of the new_folder_path', new_folder_path )
            os.makedirs(new_folder_path, exist_ok=True)
            
            # Move the image to the new folder
            old_image_path = image_instance.image.path
            new_image_path = os.path.join(new_folder_path, os.path.basename(old_image_path))
            os.rename(old_image_path, new_image_path)
            print('old_image_path', old_image_path)
            print('new_image_path', new_image_path)
            
            # Update image path in the database
            image_instance.image.name = os.path.join('uploads', new_folder_name, os.path.basename(new_image_path))
            print('image_instance.image.name', image_instance.image.name)
            image_instance.save()
            # Open the image using PIL
            img = Image.open(image_instance.image)
            # add the enrollment function below
            print(np.array(img).size)
            return HttpResponse(serializer.data, content_type="image/png")
            #return Response(, status=status.HTTP_201_CREATED)
        else:
            print('errorssss....', serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ImageUploadRecog(APIView):
    def post(self, request):
        serializer = ImageUploadSerializer(data=request.data)
        if serializer.is_valid():
            image = serializer.validated_data['image']
            image_name = default_storage.save(image.name, ContentFile(image.read()))
            print('image_name',image_name)
            image_path = os.path.join(settings.MEDIA_ROOT, image_name)
            
            # Open the image using PIL
            img = Image.open(image_path)


            # Perform some processing (e.g., convert to grayscale)
            processed_image = img.convert('L')  # Example: Convert to grayscale

            # Save the processed image
            processed_image_path = os.path.join(settings.MEDIA_ROOT,'recog_images')
            print('processed_image_path', processed_image_path)
            
            os.makedirs(processed_image_path, exist_ok=True)
            processed_image_path=os.path.join(processed_image_path,  f'processed_{image_name}')
            print('processed_image_path new:', processed_image_path)
            processed_image.save(processed_image_path)
            #deleting original image file
            os.remove(image_path)
            # Prepare response with the processed image
            with open(processed_image_path, 'rb') as img_file:
                return HttpResponse(img_file.read(), content_type="image/png")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ImageProcessingView(APIView):
    def post(self, request):
        image_id = request.data('image_id')
        try:
            image_instance = UploadedImage.objects.get(id=image_id)
            image_path = image_instance.image.path
            
            # Open the image
            img = Image.open(image_path)
            
            # Example processing: Apply a blur filter
            img = img.filter(ImageFilter.BLUR)
            
            # Save the processed image (overwriting the original or creating a new one)
            processed_image_path = image_path.replace('.jpg', '_processed.jpg')
            img.save(processed_image_path)
            
            return Response({'message': 'Image processed successfully', 'processed_image': processed_image_path})
        except UploadedImage.DoesNotExist:
            return Response({'error': 'Image not found'}, status=404)
