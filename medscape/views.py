from rest_framework import viewsets,status
from django.shortcuts import render,redirect,get_object_or_404
from rest_framework.response import Response
from django.conf import settings

from .serializers import *

from PIL import Image
import os

from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import tensorflow as tf
from tensorflow.keras.applications.vgg16 import VGG16
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.vgg16 import preprocess_input
import numpy as np

class PneumoniaViewSet(viewsets.ModelViewSet):
    queryset=Pneumonia.objects.all()
    serializer_class=PneumoniaSerializer

    def create(self, request, *args, **kwargs):
        image_file = request.FILES.get('image')

        if not image_file:
            return Response({'error': 'No image file uploaded'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            img = Image.open(image_file)
            img.verify()
        except Exception as e:
            return Response({'error': 'Invalid image file'}, status=status.HTTP_400_BAD_REQUEST)

        result = 1

        pneumonia = Pneumonia(image=image_file, result=result)
        pneumonia.save()

        image_url = pneumonia.image.url
        relative_path = image_url[len(settings.MEDIA_URL):]
        image_url = os.path.join(settings.MEDIA_ROOT, relative_path)
        print(image_url)

        model = VGG16(weights='imagenet', include_top=False)
        image_path = image_url
        image = load_img(image_path, target_size=(224, 224))
        image = img_to_array(image)
        image = np.expand_dims(image, axis=0)
        image = preprocess_input(image)
        feature = model.predict(image)
        feature = np.expand_dims(feature, axis=1)

        model = load_model('pneumonia.h5')
        result = model.predict(feature)

        result=float(result)
        pneumonia.result = result
        pneumonia.save()

        return redirect('result', pk=pneumonia.pk)


def upload(request):
    return render(request,'index.html')


def result(request, pk):
    pneumonia_instance = get_object_or_404(Pneumonia, pk=pk)
    return render(request, 'display.html', {'pneumonia_instance': pneumonia_instance})