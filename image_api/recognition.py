"""
from pathlib import Path
import os
import face_recognition
import pickle
from django.conf import settings
from PIL import Image, ImageDraw
from collections import Counter
import numpy as np

BOUNDING_BOX_COLOR = "blue"
TEXT_COLOR = "white"

DEFAULT_ENCODINGS_PATH = settings.FACE_MODEL_ROOT
with DEFAULT_ENCODINGS_PATH.open(mode="rb") as f:
    loaded_encodings = pickle.load(f)

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

  image = face_recognition.load_image_file(current_img_pat)
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

  pillow_image = Image.fromarray(image)
  draw = ImageDraw.Draw(pillow_image)
  _display_face(draw, face_locations[0], name)
  return pillow_image"""


