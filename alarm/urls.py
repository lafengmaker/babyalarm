from django.conf.urls import patterns,url
import views
urlpatterns=patterns('',
                     url(r'^$',views.index,name='index'),
                     url(r'^babyitem/(?P<baby_id>\d+)/$',views.babyitemdetail,name="babyitemlist"),
                     )