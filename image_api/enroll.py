from pathlib import Path
import os
import face_recognition
import pickle
from django.conf import settings
from PIL import Image
import numpy as np
import cv2

DEFAULT_ENCODINGS_PATH = os.path.join(settings.FACE_MODEL_ROOT, 'encodings_updated.pkl')
print('DEFAULT_ENCODINGS_PATH...:', DEFAULT_ENCODINGS_PATH)
def img_resize(img_path):
  print('img_path img_resize function', img_path)
  img = cv2.imread(str(img_path), cv2.IMREAD_COLOR)
  (h, w) = img.shape[:2]
  print('image...shape....', img.shape)

  # Desired wid0th
  new_width = 200

  # Calculate the aspect ratio
  aspect_ratio = h / w
  new_height = int(new_width * aspect_ratio)

  # Resize the image
  resized_image = cv2.resize(img, (new_width, new_height))
  print('image resized...')
  return resized_image

def Enrollment_Face(enrolled_img, enrolled_name):
  #enrolled_name='xyz'
  print('Enrollment function starts...')
  with open(DEFAULT_ENCODINGS_PATH, mode="rb") as f:
    loaded_encodings = pickle.load(f)
  names=loaded_encodings['names']
  encodings=loaded_encodings['encodings']
  print('type of enrolled_img ', type(enrolled_img))
  for i in enrolled_img:
    print('i...', i)
    print('MEDIA ROOT path', settings.MEDIA_ROOT)
    i=os.path.join(str(settings.MEDIA_ROOT), str(i))
    print('img_path for img_resize function', i)
    image = img_resize(i)
    #image= face_recognition.load_image_file(i)
    face_locations = face_recognition.face_locations(image, model='hog')
    face_encodings = face_recognition.face_encodings(image, face_locations)
    names.append(enrolled_name)
    encodings.append(face_encodings[0])
    print('appending encoding file')

  name_encodings = {"names": names, "encodings": encodings}
  with open(DEFAULT_ENCODINGS_PATH, mode="wb") as f:
    pickle.dump(name_encodings, f)
  print('data saved successfully')
  return {'resp':'The data saved successfully'}


def Enrollment_Face_updated(enrolled_img_path, enrolled_id):
  #enrolled_name='xyz'
  print('Enrollment function starts...')
  with open(DEFAULT_ENCODINGS_PATH, mode="rb") as f:
    loaded_encodings = pickle.load(f)
  enrolled_id_list=loaded_encodings['enrolled_id']
  encodings=loaded_encodings['encodings']
  print('type of enrolled_img ', type(enrolled_img_path))
  for i in enrolled_img_path:
    print('i...', i)
    print('MEDIA ROOT path', settings.MEDIA_ROOT)
    i=os.path.join(str(settings.MEDIA_ROOT), str(i))
    print('img_path for img_resize function', i)
    image = cv2.imread(str(i), cv2.IMREAD_COLOR)
    #image= face_recognition.load_image_file(i)
    face_locations = face_recognition.face_locations(image, model='hog')
    if len(face_locations)==0:
      return 'No face detected...', 0
    face_encodings = face_recognition.face_encodings(image, face_locations)
    enrolled_id_list.append(enrolled_id)
    encodings.append(face_encodings[0])
    print('appending encoding file')

  name_encodings = {"enrolled_id": enrolled_id_list, "encodings": encodings}
  with open(DEFAULT_ENCODINGS_PATH, mode="wb") as f:
    pickle.dump(name_encodings, f)
  print('data saved successfully')
  return 'The data saved successfully', 1