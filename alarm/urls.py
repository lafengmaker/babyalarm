from django.conf.urls import patterns,url
import views
urlpatterns=patterns('',
                     url(r'^$',views.index,name='index'),
                     url(r'^babyitem/(?P<baby_id>\d+)/(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})$',views.babyitemdetail,name="babyitemlist"),
                     url(r'^babyinfo/(?P<baby_id>\d+)/$',views.babyInfo,name="babyinfo"),
                     )