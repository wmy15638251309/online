from django.conf.urls import url
from apps.organization.views import *
urlpatterns = [
    url(r'^org_list/$', OrgListView.as_view(), name="org_list"),
    url(r'^ask_task/$', AskTaskView.as_view(), name="ask_task"),
    url(r'^home/(?P<org_id>\d+)/$',OrgHomeView.as_view(), name="home"),
    url(r'^course/(?P<org_id>\d+)/$', OrgCourseView.as_view(), name='course'),
    url(r'^desc/(?P<org_id>\d+)/$', OrgDescView.as_view(), name='org_desc'),
    url(r'^tea/(?P<org_id>\d+)/$', OrgTeacherView.as_view(), name='tea'),
    url(r'^add_fav/$', AddFavView.as_view(), name='add_fav'),
]

