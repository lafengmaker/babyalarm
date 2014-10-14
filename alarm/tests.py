from django.test import TestCase
import datetime
# Create your tests here.


# itemlist=AlarmItem.objects.filter(baby_id=4,itemTime__gt=datetime.datetime.now(),itemTime__lt=sevendaylater);
# for item in itemlist:
#     from django.utils.timezone import utc
#     d1 = datetime.datetime.utcnow().replace(tzinfo=utc)
#     print (item.itemTime-

d1=datetime.datetime.now();
d2=d1+datetime.timedelta(seconds=10,days=1);
print (d2-d1).days;
print (d2-d1).seconds;