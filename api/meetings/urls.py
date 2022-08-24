from django.urls import path
from .views import *

urlpatterns = [
    path('', GeneralView.as_view(), name='index'),
    path('meeting/<str:room_name>/<str:user_name>/', meeting, name='meeting'),
]