from users.views import *
from django.conf.urls import url
urlpatterns = [
    url(r'^info/$', UserCenterView.as_view(), name='center'),

    url(r'^logout/$',LogoutView.as_view(),name='logout'),
    # 用户头像修改
    url(r'^image/upload/$', UploadImageView.as_view(), name='image_upload'),

    # 用户个人中心修改密码
    url(r'^update/pwd/$', UpdatePwdView.as_view(), name='update_pwd'),

    # 修改邮箱时 发送邮箱验证码
    url(r'^sendemail_code/$', SendEmailCodeView.as_view(), name='sendemail_code'),

    # 修改邮箱时，验证邮箱和验证码
    url(r'^update_email/$', UpdateEmailView.as_view(), name='update_email'),

    # 我的课程
    url(r'^mycourse/$', MyCourseView.as_view(), name='mycourse'),

    # 我收藏的课程机构
    url(r'^myfav/org/$', MyFavOrgView.as_view(), name='myfav_org'),

    # 我收藏的授课讲师
    url(r'^myfav/teacher/$', MyFavTeacherView.as_view(), name='myfav_teacher'),

    # 我收藏的课程
    url(r'^myfav/course/$', MyFavCourseView.as_view(), name='myfav_course'),

    url(r'^message/$',MessageView.as_view(),name='message'),
]
