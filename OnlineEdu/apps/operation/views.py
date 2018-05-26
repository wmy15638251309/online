from django.shortcuts import render,HttpResponse
from django.views.generic.base import View
import json
from courses.models import Course
from organization.models import CourseOrg
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from users.models import Banner
# Create your views here.


class IndexView(View):
    def get(self,request):
        banner_list = Banner.objects.all()
        org_list = CourseOrg.objects.all().order_by('-click_nums')
        course_list = Course.objects.all().order_by('-click_nums')

        return render(request, 'index.html', {'banner_list':banner_list,'org_list': org_list,'course_list':course_list})