# coding=utf8
from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from alarm.models import Baby,AlarmItem
import datetime
# Create your views here.
def index(request):
    babylist=Baby.objects.all().order_by("id")
    return render(request,'index.html',{"babylist":babylist});

def babyitemdetail(request,baby_id):
    baby=get_object_or_404(Baby, pk=baby_id)
    sevendaylater=datetime.datetime.now()+datetime.timedelta(days=7);
    itemlist=AlarmItem.objects.filter(baby_id=baby_id,itemTime__gt=datetime.datetime.now(),itemTime__lt=sevendaylater);
    return render(request,'itemlist.html',{"itemlist":itemlist});
        
    