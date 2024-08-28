from django.db import models

class UploadedImage(models.Model):
    image = models.ImageField(upload_to='uploads/')
    name = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)

from django.db import models
from django.core.exceptions import ValidationError

class Person(models.Model):
    image = models.ImageField(upload_to='uploads/')
    name = models.CharField(max_length=100)
    father_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()

    class Meta:
        unique_together = ('name', 'father_name', 'date_of_birth')

    def __str__(self):
        return f"{self.name} - {self.father_name} - {self.date_of_birth}"

    def save(self, *args, **kwargs):
        # Ensure that the combination is unique before saving
        if Person.objects.filter(name=self.name, father_name=self.father_name, date_of_birth=self.date_of_birth).exists():
            raise ValidationError("This combination of name, father_name, and date_of_birth already exists.")
        super(Person, self).save(*args, **kwargs)
