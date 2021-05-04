from django.urls import path
from . import views

app_name = 'notifys'

urlpatterns = [
    path('notifys/<int:id>/', views.notifys_detail, name='notifys_detail'),
]