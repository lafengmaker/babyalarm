# coding=utf8
from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse
from alarm.models import Baby,AlarmItem
import datetime,time
import ChineseCalendar
# Create your views here.
class itemshow():
    def __init__(self,itemTime,itemName):
        self.dt=itemTime;
        self.name=itemName;
        self.time= datetime.datetime.strftime(itemTime,'%Y-%m-%d %H:%M:%S')
        from django.utils.timezone import utc
        d1 = datetime.datetime.utcnow().replace(tzinfo=utc)
        self.remainsec=((itemTime-d1).seconds);
        self.remainday=((itemTime-d1).days);
class DateIem():
    def __init__(self,date):
        (self.gy,self.gm,self.gd)=(date.year,date.month,date.day);
        (self.ny,self.nm,self.nd)=ChineseCalendar.get_ludar_date(date);
        self.nd=ChineseCalendar.d_lunar(self.nd);
        self.w=w=int(date.strftime('%w'));
        self.dt=date;
        self.items="";
        
def loandweekday(dt_s,num):
    li=[];
    for i in range(0,num):
        li.append(DateIem(dt_s));
        deltaw=datetime.timedelta(days=1);
        dt_s=dt_s+deltaw;
    return li;
def comparedate(d1,d2,type):
    if  type == 1 :
        return True;
    (y1,m1,da1,w1)=(d1.year,d1.month,d1.day,int(d1.strftime('%w')));
    (y2,m2,da2,w2)=(d2.year,d2.month,d2.day,int(d1.strftime('%w')));
    if type == 3 :#monthly
        return da1 == da2;
    elif type ==4:#yearly
        return da1==da2 and m1 == m2;
    elif type ==2:
        return w1==w2;
    else:#once
        return y1==y2 and da1==da2 and m1 == m2;
        
def getWeeksratDay(dt):
    w=int(dt.strftime('%w'))-1;
    deltaw=datetime.timedelta(days=w);
    dt_s=dt-deltaw;
    return dt_s;
def getCalenderStart(dt):
    dt_s=getWeeksratDay(dt);
    deltaw=datetime.timedelta(days=7);
    dt_s=dt_s-deltaw;
    return dt_s;
def getMonthdayList(dt):
    dt_s=getWeeksratDay(dt);
    dt_s=getCalenderStart(dt_s);
    li=loandweekday(dt_s,35);
    return li;
    
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
    (y,m,x)=ChineseCalendar.get_ludar_date(date);
    return y;
def date2dateTime(date):
     (y,m,d)=(date.year,date.month,date.day)
     return datetime.datetime(y,m,d);
def date2utcdateTime(date):
     (y,m,d)=(date.year,date.month,date.day)
     from django.utils.timezone import utc
     d1 = datetime.datetime.utcnow().replace(tzinfo=utc)
     return d1.replace(year=y,month=m,day=d);
def getYearsVirtual(d):
    y1=getLYear(datetime.datetime.now());
    y2=getLYear(date2dateTime(d));
    return (y1-y2)+1;

def index(request):
    now=datetime.datetime.now();
    if 'baby_id' in request.COOKIES:
        baby_id = request.COOKIES['baby_id']
        if request.GET :
            dt=request.GET['dt'];            
            if dt:
                t= time.strptime(dt, "%Y-%m-%d")
                now=datetime.datetime(*t[:3]);
        return redirect('babyitemlist',baby_id=baby_id,year=now.year,month=now.month,day=now.day);
    babylist=Baby.objects.all().order_by("id")
    return render(request,'index.html',{"babylist":babylist,"now":now});

def babyitemdetail(request,baby_id,year,month,day):
    if not baby_id :
        return redirect('index');
    try:
        currdat=datetime.datetime(int(year),int(month),int(day));
    except:
        render(request,'error.html',{"msg":"日期格式不正确"});
    baby=get_object_or_404(Baby, pk=baby_id)
    now = date2utcdateTime(currdat);
    rnow=datetime.datetime.now();
    dt_start=getCalenderStart(currdat);
    dt_end=dt_start+datetime.timedelta(days=35);
    itemlist=AlarmItem.objects.filter(baby_id=baby_id,itemTime__gt=dt_start,itemTime__lt=dt_end);
    dayli=getMonthdayList(currdat);
    start_d=getWeeksratDay(currdat);
    
    babytime=date2utcdateTime(baby.birthday);
    for dayi in dayli:
        if comparedate(dayi.dt,baby.birthday,4):
            dayi.items=dayi.items+"宝宝过生日";
            #dayi.isli.append(itemshow(babytime,"宝宝过生日"));
        for item in itemlist:
            if comparedate(dayi.dt,item.itemTime,int(item.itemInterval)):
                dayi.items=dayi.items+item.itemName.encode('utf-8');
                #dayi.isli.append(itemshow( item.itemTime,item.itemName));
    #response = render(request,'itemlist.html',{"now":now,"dinfo":{"g":datetime.date.strftime(now,"%Y年%m月%d日"),"gi":datetime.date.strftime(now,"%Y-%m-%d"),"n":ChineseCalendar.getChinesestr(datetime.datetime.now())},  "dayli":dayli,"babydays":(babyyd.days+1),"babyyearsv":babyyearv,"babyyears":babyyear,"birthday":datetime.date.strftime(baby.birthday,"%Y-%m-%d"),"baby":baby});
    response = render(request,'itemlist.html',{"now":now,
                                               "dinfo":{"g":datetime.date.strftime(now,"%Y年%m月%d日"),"gi":datetime.date.strftime(now,"%Y-%m-%d"),"n":ChineseCalendar.getChinesestr(currdat)},
                                                "dayli":dayli,
                                                "isToday":comparedate(rnow,currdat,5),
                                                "baby":baby});
    response.set_cookie('baby_id', baby_id);
    return response ;

def babyInfo(request,baby_id):
    if not baby_id :
        return redirect('index');
    baby=get_object_or_404(Baby, pk=baby_id)
    dnow = datetime.date.today()
    babyyd=(dnow-baby.birthday);
    babyyear=getYearCircle(baby.birthday);
    babyyearv=getYearsVirtual(baby.birthday);
    return render(request,'babyinfo.html',{"baby":baby,"babyyd":babyyd,"babyyear":babyyear,"babyyearv":babyyearv});
    
    
    
        

