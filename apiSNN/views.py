#CONTROLADOR

from rest_framework import generics #para microservicio
from apiSNN import models
from apiSNN import serializers
import os
from django.core.files.storage import FileSystemStorage
from werkzeug.datastructures import FileStorage
from django.shortcuts import render
import pyrebase #para consumo servicio base de datos de firebase
from apiSNN.Logica import modeloSNN #para utilizar modelo.json SNN
from apiSNN.Logica import controlador

# Create your views here.
class ListLibro(generics.ListCreateAPIView):
    """
    retrieve:
        Retorna una instancia libro.

    list:
        Retorna todos los libros, ordenados por los más recientes.

    create:
        Crea un nuevo libro.

    delete:
        Elimina un libro existente.

    partial_update:
        Actualiza uno o más campos de un libro existente.

    update:
        Actualiza un libro.
    """
    queryset = models.Libro.objects.all()
    serializer_class = serializers.LibroSerializer

class DetailLibro(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Libro.objects.all()
    serializer_class = serializers.LibroSerializer

class ListPersona(generics.ListCreateAPIView):
    queryset = models.Persona.objects.all()
    serializer_class = serializers.PersonaSerializer

class DetailPersona(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Persona.objects.all()
    serializer_class = serializers.PersonaSerializer

config = {

    'apiKey': "AIzaSyDBYpL2tb3yh3SIPo2BFhlS7slKruVGOic",
    'authDomain': "proyectotiendajpri.firebaseapp.com",
    'databaseURL': "https://proyectotiendajpri.firebaseio.com",
    'projectId': "proyectotiendajpri",
    'storageBucket': "proyectotiendajpri.appspot.com",
    'messagingSenderId': "1046831721926",
    'appId': "1:1046831721926:web:7402a636a8cd165f4b16c7",
    'measurementId': "G-MKSCN84RDE"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()

class Autenticacion():

    def upload(request):
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        if request.method == 'POST':
            archivo = request.FILES['archivo']
            fileStorage = FileSystemStorage()
            fileStorage.save(archivo.name, archivo)

            url_imagen = BASE_DIR + '/' + archivo.name
            Imagen, porcentaje = controlador.predecirImg(url_imagen)
            return render(request, "prediccion.html", {'Imagen': Imagen, 'porcentaje': porcentaje})

        return render(request, "index.html")


    def singIn(request):

        return render(request, "signIn.html")

    def postsign(request):
        email=request.POST.get('email')
        passw = request.POST.get("pass")
        try:
            user = auth.sign_in_with_email_and_password(email,passw)
        except:
            message = "invalid cerediantials"
            return render(request,"signIn.html",{"msg":message})
        print(user)
        return render(request, "welcome.html",{"e":email})

class Clasificacion():
    #imagen = models.ImageField(upload_to='imagenes')
    #prediccion = models.CharField(max_length=200, blank=True)

    def determinarSobrevivencia(request):

        return render(request, "sobrevivencia.html")

    def predecir(request):
        try:
            pclass = int(request.POST.get('pclass'))
            sex = request.POST.get('sex')
            age = int(''+request.POST.get('age'))
            fare = float(request.POST.get('fare'))
            embarked = request.POST.get('embarked')
        except:
            pclass=2
            sex='female'
            age=60
            fare=6670
            embarked='C'
        print(type(age))
        #resul=modeloSNN.modeloSNN.suma(num1,num2)
        resul=modeloSNN.modeloSNN.predecirSobrevivencia(modeloSNN.modeloSNN,pclass,sex,age,fare,embarked)
        
        return render(request, "welcome.html",{"e":resul})