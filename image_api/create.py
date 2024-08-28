import pickle
name_encodings = {"enrolled_id": [], "encodings": []}
with open('/home/faceapp/new_fr/image_processor/face_recog_model/encodings_updated.pkl' , mode="wb") as f:
  pickle.dump(name_encodings, f)
  print('file saved successfully...')