from django.core.files.storage import FileSystemStorage
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
import numpy as np
import keras
import tensorflow
from keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.models import load_model
import os


# Create your views here.

def index(request):
    data = {'titulo': 'Detección Objetos'}

    template = loader.get_template('index.html')
    return HttpResponse(template.render(data))


def cargarImagenes(request):

    if request.method == "POST":
        # if the post request has a file under the input name 'document', then save the file.
        request_file = request.FILES['document'] if 'document' in request.FILES else None
        if request_file:
            # save attatched file

            # create a new instance of FileSystemStorage
            fs = FileSystemStorage()
            file = fs.save(request_file.name, request_file)
            # the fileurl variable now contains the url to the file. This can be used to serve the file when needed.
            fileurl = fs.url(file)


    data = {'titulo': 'hola'}



    template = loader.get_template('cargarImagenes.html')
    return HttpResponse(template.render(data, request))


def reconocimientoObjetos(request):
    data = {'titulo': 'hola'}
    template = loader.get_template('reconocimientoObjetos.html')
    return HttpResponse(template.render(data))


def video(request):

    imagen = None
    imgr = "static/imagenes/"
    longitud, altura = 150, 150
    modelo = './modelo/modelo.h5'
    pesos_modelo = './modelo/pesos.h5'
    cnn = load_model(modelo)
    cnn.load_weights(pesos_modelo)

    def predict(file):

        x = load_img(file, target_size=(longitud, altura))
        x = img_to_array(x)
        x = np.expand_dims(x, axis=0)
        array = cnn.predict(x)
        result = array[0]
        print(result)
        answer = np.argmax(result)
        if answer == 0:
            answer="Botella"
        elif answer == 1:
            answer="Organico"
        elif answer == 2:
            answer="Pitillo"
        elif answer == 3:
            answer="Toxico"

        os.remove("static/imagenes/" + imagen)

        return answer

    if not os.listdir("static/imagenes"):
        print("No tiene imagenes")
    else:
        for i in os.listdir("static/imagenes"):
            imagen = i


    prediccion = predict(imgr + imagen)
    data = {'titulo': 'Detección Objetos', 'predict': prediccion}

    template = loader.get_template('video.html')
    return HttpResponse(template.render(data))
