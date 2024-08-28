import os
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import UploadedImage,Person
from django.shortcuts import get_object_or_404
from .serializers import UploadedImageSerializer,ImageUploadSerializer,PersonSerializer
from .enroll import Enrollment_Face, img_resize, Enrollment_Face_updated
from .recognition import recog_face,recog_face_updated
from django.conf import settings
from PIL import Image, ImageFilter
from django.http import HttpResponse
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import numpy as np
import cv2
import pickle
import shutil

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
            enrolled_img = image_instance.image
            enrolled_name=image_instance.name
            print('enrolled_img:...', enrolled_img)
            print('enrolled_name:...', enrolled_name)
            #the function below takes a list of images path, 
            #As there is a single image, so convert the image into list
            Enrollment_Face([enrolled_img], enrolled_name)
            # add the enrollment function below
            print('Enrollement completed')
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
            DEFAULT_ENCODINGS_PATH = os.path.join(settings.FACE_MODEL_ROOT, 'encodings_updated.pkl')
            with open(DEFAULT_ENCODINGS_PATH, mode="rb") as f:
                loaded_encodings = pickle.load(f)

            processed_image=recog_face_updated(loaded_encodings, image_path)
            if isinstance(processed_image,str):
                return HttpResponse(processed_image, content_type="text/plain")
            print('recog_face function executed')
            # Open the image using PIL
            #img = Image.open(image_path)


            # Perform some processing (e.g., convert to grayscale)
            #processed_image = img.convert('L')  # Example: Convert to grayscale

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



def get_person_details(unique_id):
    # Fetch the person object using the unique ID (primary key)
    person = get_object_or_404(Person, id=unique_id)
    
    # Return the name, father_name, and date_of_birth fields
    return {
        'name': person.name,
        'father_name': person.father_name,
        'date_of_birth': person.date_of_birth,
    }

def get_unique_id(name, father_name, date_of_birth):
    # Try to get the person object matching the given criteria
    person = get_object_or_404(Person, name=name, father_name=father_name, date_of_birth=date_of_birth)
    
    # Return the primary key (id) of the person
    return person.id
def delete_person_by_id(person_id):
    # Attempt to retrieve and delete the person by their unique ID
    person = get_object_or_404(Person, id=person_id)
    person.delete()
    print('no face detected so rolling back the data...')

class ImageEnroll(APIView):
    def post(self, request):
        print('request', request)
        serializer = PersonSerializer(data=request.data)
        print('data', request.data)
        if serializer.is_valid():
            print('The if statemtent hit...')
            serializer.save()
            enroll_serializer = serializer.instance
            print('image name...::', enroll_serializer.image.name)
            print('image path...::', enroll_serializer.image.path)
            print(enroll_serializer.name, enroll_serializer.father_name, enroll_serializer.date_of_birth)
            person_id=get_unique_id(enroll_serializer.name, enroll_serializer.father_name, enroll_serializer.date_of_birth)
            
            new_folder_name=f'{person_id}_{enroll_serializer.name.replace(" ", "")}'
            new_folder_path = os.path.join(settings.MEDIA_ROOT, 'Enroll', new_folder_name)
            os.makedirs(new_folder_path, exist_ok=True)
            image_resize=img_resize(enroll_serializer.image.path)
            print('image resized size...',image_resize.size)
            new_img_path=os.path.join(new_folder_path, enroll_serializer.image.name.split('/')[-1])
            print('new_img_path', new_img_path)
                                      
            cv2.imwrite(new_img_path, image_resize)
            print('removed image...')
            os.remove(enroll_serializer.image.path)
            # add the enrollment function below
            print('person_id::..', person_id)
            message, fd=Enrollment_Face_updated([new_img_path], str(person_id))
            if fd==0:
                delete_person_by_id(person_id)

            return HttpResponse(message, content_type="text/plain")
            #return Response(, status=status.HTTP_201_CREATED)
        else:
            print('errorssss....', serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
