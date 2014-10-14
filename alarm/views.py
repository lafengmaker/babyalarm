# coding=utf8
from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse
from alarm.models import Baby,AlarmItem
import datetime,time
# Create your views here.
class itemshow():
    def __init__(self,name,ptime):
        self.name=name;
        self.time= datetime.datetime.strftime(ptime,'%Y-%m-%d %H:%M:%S')
        from django.utils.timezone import utc
        d1 = datetime.datetime.utcnow().replace(tzinfo=utc)
        self.remainsec=((ptime-d1).seconds);
        self.remainday=((ptime-d1).days);
def getYearCircle(d):
    (y,m,d)=(d.year,d.month,d.day)
    d2=datetime.date.today();
    y2=d2.year;
    ddlta=(d2-datetime.date(y2,m,d)).days;
    if ddlta>=0:
        return y2-y;
    else:
        return y2-y-1;
def getLYear(date):
    import ChineseCalendar
    (y,m,x)=ChineseCalendar.get_ludar_date(date);
    return y;
def date2dateTime(date):
     (y,m,d)=(date.year,date.month,date.day)
     return datetime.datetime(y,m,d);
def getYearsVirtual(d):
    y1=getLYear(datetime.datetime.now());
    y2=getLYear(date2dateTime(d));
    return (y1-y2)+1;
    
def index(request):
    if 'baby_id' in request.COOKIES:
        baby_id = request.COOKIES['baby_id']
        return redirect('babyitemlist',baby_id=baby_id);
    babylist=Baby.objects.all().order_by("id")
    return render(request,'index.html',{"babylist":babylist});

def babyitemdetail(request,baby_id):
    baby=get_object_or_404(Baby, pk=baby_id)
    from django.utils.timezone import utc
    now = datetime.datetime.utcnow().replace(tzinfo=utc)
    sevendaylater=now+datetime.timedelta(days=7);
    dnow = datetime.date.today()
    babyyd=(dnow-baby.birthday);
    babyyear=getYearCircle(baby.birthday);
    babyyearv=getYearsVirtual(baby.birthday);
    itemlist=AlarmItem.objects.filter(baby_id=baby_id,itemTime__gt=datetime.datetime.now(),itemTime__lt=sevendaylater);
    li=[];
    for item in itemlist:
        li.append(itemshow(item.itemName, item.itemTime));
    response = render(request,'itemlist.html',{"itemlist":li,"babydays":(babyyd.days+1),"babyyearsv":babyyearv,"babyyears":babyyear,"birthday":datetime.date.strftime(baby.birthday,"%Y-%m-%d"),"baby":baby});
    response.set_cookie('baby_id', baby_id);
    return response ;
        
