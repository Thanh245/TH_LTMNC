from django.shortcuts import render, get_object_or_404
from .models import *


# Create your views here.

def notifys_detail(request, id):
    notifys = get_object_or_404(Notify, pk=id)
    return render(request, "notifys/notifys.html", {'notifys': notifys})
