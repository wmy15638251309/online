from django.conf.urls import url,include
from .views import *
from django.views.static import serve
from OnlineEdu.settings import MEDIA_ROOT



urlpatterns = [
    url(r'^list/$', CourseListView.as_view(), name="course_list"),
    url(r'^detail/(?P<course_id>\d+)/$', CourseDetailView.as_view(), name='detail'),
    url(r'^info/(?P<course_id>\d+)/$', CourseInfoView.as_view(), name='info'),# 课程章节信息
    url(r'^comment/(?P<course_id>\d+)/$', CommentView.as_view(), name='course_comment'),
    url(r'^add/$', AddCommentView.as_view(), name='add_comment'),
    url(r'^video/(?P<video_id>\d+)/$', VideoPlayView.as_view(), name='video_play'),
    url(r'^tea_list/$', TeacherListView.as_view(), name="tea_list"),
    url(r'^tea_detail/(?P<teacher_id>\d+)/$', TeacherDetailView.as_view(), name="tea_detail"),
    # url(r'^add_fav/$', AddFavView.as_view(), name='add_fav'),

]
