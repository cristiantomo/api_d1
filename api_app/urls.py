from django.urls import path
from .views import CollaborativeFilter

urlpatterns = [
        path('collaborative/<int:pk>', CollaborativeFilter),
]
