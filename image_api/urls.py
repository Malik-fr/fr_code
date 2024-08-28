from django.urls import path
from .views import ImageUploadView, ImageUploadRecog,ImageEnroll

urlpatterns = [
    path('upload/', ImageUploadView.as_view(), name='image-upload'),
    #path('process/', ImageProcessingView.as_view(), name='image-process'),
    path('enroll/', ImageEnroll.as_view(), name='enroll'),
    path('recog/', ImageUploadRecog.as_view(), name='image-recog')

]

