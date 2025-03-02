from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('registrar_gasto/', views.registrar_gasto, name="registrar_gasto"),
    path('lista', views.lista, name='lista'),
]
