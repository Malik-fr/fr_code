from django.db import models

class UploadedImage(models.Model):
    image = models.ImageField(upload_to='uploads/')
    name = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)
