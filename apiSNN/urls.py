# existing imports
from django.urls import path
from django.conf.urls import url
from apiSNN import views

urlpatterns = [
    url(r'^predecir/',views.Clasificacion.predecir),
    url(r'^$',views.Autenticacion.singIn),
    url(r'^postsign/',views.Autenticacion.postsign),
    url(r'^', views.Autenticacion.upload),
]