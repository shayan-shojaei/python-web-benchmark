from django.urls import path
from . import views

urlpatterns = [
    path('', views.mongo_crud, name='mongo_crud'),
    path('<str:id>', views.mongo_detail, name='mongo_detail'),
]
