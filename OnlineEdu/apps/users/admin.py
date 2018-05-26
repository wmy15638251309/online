from django.contrib import admin
from .models import *
import xadmin
from xadmin import views
# Register your models here.
# class UserProfileAdmin(admin.ModelAdmin):
#     pass
# admin.site.register(UserProfile,UserProfileAdmin)
# admin.site.register(EmailVerifyRecord)
# admin.site.register(Banner)


class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True

xadmin.site.register(views.BaseAdminView, BaseSetting)


class GlobalSettings(object):
    site_title = "硅谷后台管理系统"
    site_footer = "硅谷在线网"
    menu_style = "accordion"

xadmin.site.register(views.CommAdminView, GlobalSettings)