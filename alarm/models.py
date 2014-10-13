# coding=utf8
from django.db import models
from django.db.models.fields import CharField
from test.test_imageop import MAX_LEN
sextuple = (("1","男"),("0","女"))
itemIntervaltuple=(("0","提醒一次"),("1","每天"),("2","每周"),("3","每月"),("4","每年"))
# Create your models here.
class Baby(models.Model):
    name = models.CharField(max_length=50)
    birthday = models.DateField()
    sex = models.CharField(max_length=1,choices=sextuple);
    def __str__(self):
        return self.name.encode('utf-8')
    
class AlarmItem(models.Model):
    itemName = models.CharField(max_length=100)
    itemTime = models.DateTimeField()
    itemInterval = models.CharField(max_length=2,choices=itemIntervaltuple)
    baby = models.ForeignKey(Baby)
    def __str__(self):
        return self.itemName.encode('utf-8')

 