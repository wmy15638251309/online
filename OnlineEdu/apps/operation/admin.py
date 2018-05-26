from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(UserAsk)
admin.site.register(CourseComments)
admin.site.register(UserFavorite)
admin.site.register(UserMessage)
admin.site.register(UserCourse)