from django.urls import path
from . import views

urlpatterns = [
    path('', views.postgres_crud, name='postgres-crud'),
    path('<int:pk>', views.postgres_detail, name='postgres-detail'),
]
