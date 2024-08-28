from pathlib import Path
import os
import face_recognition
import pickle
from django.conf import settings
from PIL import Image, ImageDraw
from collections import Counter
import numpy as np
from .enroll import img_resize
import cv2
from django.shortcuts import get_object_or_404
from .models import Person

BOUNDING_BOX_COLOR = "blue"
TEXT_COLOR = "white"


def _display_face(draw, bounding_box, name):
    top, right, bottom, left = bounding_box
    draw.rectangle(((left, top), (right, bottom)), outline=BOUNDING_BOX_COLOR)
    text_left, text_top, text_right, text_bottom = draw.textbbox(
        (left, bottom), name
    )
    draw.rectangle(
        ((text_left, text_top), (text_right, text_bottom)),
        fill="blue",
        outline="blue",
    )
    draw.text(
        (text_left, text_top),
        name,
        fill="white",
    )

def recog_face(loaded_encodings, current_img_pat):
  print('recig func started')

  #image = face_recognition.load_image_file(current_img_pat)
  image = img_resize(current_img_pat)
  face_locations = face_recognition.face_locations(image, model='hog')
  face_encodings = face_recognition.face_encodings(image, face_locations)

  boolean_matches = face_recognition.compare_faces(loaded_encodings["encodings"], face_encodings[0])
  face_dist=face_recognition.face_distance(loaded_encodings["encodings"], face_encodings[0])

  votes = Counter(name for match, name in zip(boolean_matches, loaded_encodings["names"]) if match)
  confidence=1-face_dist[np.argmin(face_dist)]
  if confidence <= 0.5:
    name='unknown person'
    print(name)
  else:
    name=loaded_encodings["names"][np.argmin(face_dist)]
    print('confidence of the model is:{}'.format(confidence))
  #convert bgr to rgb color
  img_pil=cv2.cvtColor(image, cv2.COLOR_BGR2RGB) 
  pillow_image = Image.fromarray(img_pil)
  draw = ImageDraw.Draw(pillow_image)
  _display_face(draw, face_locations[0], name)
  return pillow_image

def get_person_details(unique_id):
    # Fetch the person object using the unique ID (primary key)
    person = get_object_or_404(Person, id=unique_id)
    
    # Return the name, father_name, and date_of_birth fields
    """return {
        'name': person.name,
        'father_name': person.father_name,
        'date_of_birth': person.date_of_birth,
    }"""
    return person.name
def read_enrolled_image(enr_id, name, recog_image):
   enroll_image_folder=f'{enr_id}_{name.replace(" ", "")}'
   enroll_image_path = os.path.join(settings.MEDIA_ROOT, 'Enroll', enroll_image_folder)
   enroll_image_path=os.path.join(enroll_image_path,os.listdir(enroll_image_path)[0] )
   print('enroll_image_path...', enroll_image_path)
   image1 = Image.open(enroll_image_path)
   image2 = recog_image
   # Get the sizes of the images
   width1, height1 = image1.size
   width2, height2 = image2.size

   # Create a new image with a width of both images combined and height of the taller image
   new_width = width1 + width2
   new_height = max(height1, height2)
   new_image = Image.new('RGB', (new_width, new_height))

   # Paste the images into the new image
   new_image.paste(image1, (0, 0))
   new_image.paste(image2, (width1, 0))

   # Save or show the result
   return new_image

def recog_face_updated(loaded_encodings, current_img_pat):
  print('recig func started')

  #image = face_recognition.load_image_file(current_img_pat)
  image = img_resize(current_img_pat)
  face_locations = face_recognition.face_locations(image, model='hog')
  face_encodings = face_recognition.face_encodings(image, face_locations)
  if len(face_locations)==0:
     return 'No face detected..'

  boolean_matches = face_recognition.compare_faces(loaded_encodings["encodings"], face_encodings[0])
  face_dist=face_recognition.face_distance(loaded_encodings["encodings"], face_encodings[0])

  #votes = Counter(name for match, name in zip(boolean_matches, loaded_encodings["names"]) if match)
  confidence=1-face_dist[np.argmin(face_dist)]
  if confidence <= 0.5:
    name='unknown person'
    print(name)
    img_pil=cv2.cvtColor(image, cv2.COLOR_BGR2RGB) 
    pillow_image = Image.fromarray(img_pil)
    draw = ImageDraw.Draw(pillow_image)
    _display_face(draw, face_locations[0], name)
    new_combine_image=pillow_image
  else:
    enr_id=loaded_encodings["enrolled_id"][np.argmin(face_dist)]
    name=get_person_details(enr_id)
    print('confidence of the model is:{}'.format(confidence))
    #convert bgr to rgb color
    img_pil=cv2.cvtColor(image, cv2.COLOR_BGR2RGB) 
    pillow_image = Image.fromarray(img_pil)
    draw = ImageDraw.Draw(pillow_image)
    _display_face(draw, face_locations[0], name)
    new_combine_image=read_enrolled_image(enr_id, name, pillow_image)
  return new_combine_image



