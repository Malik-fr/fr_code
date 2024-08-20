from django.urls import path
from .views import ImageUploadView,ImageProcessingView, ImageUploadRecog

urlpatterns = [
    path('upload/', ImageUploadView.as_view(), name='image-upload'),
    path('process/', ImageProcessingView.as_view(), name='image-process'),
    path('recog/', ImageUploadRecog.as_view(), name='image-recog')

]

