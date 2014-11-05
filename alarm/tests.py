#encoding=utf=8
from django.test import TestCase
import datetime,time
# Create your tests here.


# itemlist=AlarmItem.objects.filter(baby_id=4,itemTime__gt=datetime.datetime.now(),itemTime__lt=sevendaylater);
# for item in itemlist:
#     from django.utils.timezone import utc
#     d1 = datetime.datetime.utcnow().replace(tzinfo=utc)
#     print (item.itemTime-

# d1=datetime.datetime.now();
# d2=d1+datetime.timedelta(seconds=10,days=1);
# print (d2-d1).days;
# print (d2-d1).seconds;

# d1=datetime.datetime(2014,2,31);
# print d1
# try:
#     x="yyyyy"
# except:
#     print "====="+x;
# print "xxxx"+x

s1='2014-09-30'

t = time.strptime(s1, "%Y-%m-%d")
print t;

print type(t)
a_datetime=datetime.datetime(*t[:3]);

print a_datetime