# existing imports
from django.urls import path
from django.conf.urls import url
from apiCNN import views

urlpatterns = [
    url(r'^$',views.Autenticacion.singIn),
    url(r'^postsign/',views.Autenticacion.postsign),
    url(r'^', views.Autenticacion.upload),
]