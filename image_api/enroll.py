"""
from pathlib import Path
import os
import face_recognition
import pickle
from django.conf import settings
from PIL import Image
import numpy as np

DEFAULT_ENCODINGS_PATH = settings.FACE_MODEL_ROOT

def img_resize(img_path):
  base_width = 250
  resize_img=Image.open(img_path)
  wpercent = (base_width / float(resize_img.size[0]))
  hsize = int((float(resize_img.size[1]) * float(wpercent)))
  
  return resize_img.resize((base_width, hsize), Image.Resampling.LANCZOS)

def Enrollment_Face(enrolled_img, enrolled_name):
  #enrolled_name='xyz'
  with DEFAULT_ENCODINGS_PATH.open(mode="rb") as f:
    loaded_encodings = pickle.load(f)
  names=loaded_encodings['names']
  encodings=loaded_encodings['encodings']
  for i in enrolled_img:
    image = face_recognition.load_image_file(i)

    face_locations = face_recognition.face_locations(image, model='hog')
    face_encodings = face_recognition.face_encodings(image, face_locations)
    names.append(enrolled_name)
    encodings.append(face_encodings[0])

  name_encodings = {"names": names, "encodings": encodings}
  with DEFAULT_ENCODINGS_PATH.open(mode="wb") as f:
    pickle.dump(name_encodings, f)
  return ({'resp':'The data saved successfully'})
"""