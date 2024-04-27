from django.urls import path
from . import views 

urlpatterns = [
    path('operacional/', views.operacional, name='operacional'),
]