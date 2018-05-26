from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic.base import View
from pure_pagination import Paginator,PageNotAnInteger
from utils.mixin_utils import LoginRequiredMixin
from courses.models import Course
from operation.models import UserFavorite
from organization.forms import UserAskForm
from organization.models import CityDict, CourseOrg, Teacher
import json

# Create your views here.


class OrgListView(View):
    def get(self, request):
        city_list = CityDict.objects.all()
        courseOrg = CourseOrg.objects.all()
        org_num = courseOrg.count()
        hot_orgs = courseOrg.order_by("-click_nums")[:3]
        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            courseOrg = courseOrg.filter(
                Q(name__icontains=search_keywords) |
                Q(desc__icontains=search_keywords) |
                Q(category__icontains=search_keywords)|
                Q(course_nums__icontains=search_keywords)
            )
        category = request.GET.get("ct", "")
        if category:
            courseOrg = courseOrg.filter(category=category)
        city_id = request.GET.get('city', "")
        if city_id:
            courseOrg = courseOrg.filter(city_id=int(city_id))
        # 排序
        sort = request.GET.get('sort', "")
        if sort:
            if sort == "students":
                courseOrg = courseOrg.order_by("-students")
            elif sort == "courses":
                courseOrg = courseOrg.order_by("-course_nums")
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(courseOrg,1, request=request)
        orgs = p.page(page)

        return render(request, "org-list.html",{
            'city_list': city_list,
            'courseOrg': orgs,
            "hot_orgs": hot_orgs,
            "category": category,
            "city_id": city_id,
            "sort": sort,
            "org_num":org_num,
        })


class AskTaskView(View):
    # 组织form
     def post(self,request):
         user_ask_form = UserAskForm(request.POST)

         res = dict()
         if user_ask_form.is_valid():
            user_ask_form.save(commit=True)
            res['status']= 'success'
         else:
             res['status'] = 'fail'
             res['msg'] = '添加出错'
         return HttpResponse(json.dumps(res), content_type="application/json")


class OrgHomeView(View):
    def get(self,request,org_id):
        current_page = 'home'
        #获取机构
        course_org = CourseOrg.objects.get(id=int(org_id))
        #获取机构的课程
        all_courses = course_org.course_set.all()[:3]
        #获取机构的老师
        all_teachers  =  course_org.teacher_set.all()[:1]
        return  render(request,'org-detail-homepage.html',{
            "all_courses":all_courses,
            "all_teachers":all_teachers,
            "course_org":course_org,
            "current_page":current_page
        })


  # 课程机构详情页课程页面
class OrgCourseView(View):
      def get(self,request,org_id):
          current_page = 'course' #判断左边选择栏目
          #根据传过来的org_id 获取机构
          course_org = CourseOrg.objects.get(id=int(org_id))
          all_courses = course_org.course_set.all()
          #分页
          try:
              page = request.GET.get('page', 1)
          except PageNotAnInteger:
              page = 1

          p = Paginator(all_courses, 1, request=request)

          courses = p.page(page)

          return  render(request,'org-detail-course.html',{
              'all_courses': courses,
              'course_org': course_org,
              'current_page': current_page
          })

class OrgDescView(View):
    # 课程机构介绍页
    def get(self, request, org_id):
        current_page = 'desc'
        course_org = CourseOrg.objects.get(id=int(org_id))

        # 初始化判断是否收藏
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True

        return render(request, 'org-detail-desc.html', {
            'course_org': course_org,
            'current_page': current_page,
            'has_fav': has_fav,
        })


class OrgTeacherView(View):
    def get(self, request, org_id):
        current_page = 'teacher'
        course_org = CourseOrg.objects.get(id=int(org_id))
        all_teachers = course_org.teacher_set.all()

        # 初始化判断是否收藏
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True

        return render(request, 'org-detail-teachers.html', {
            'all_teachers': all_teachers,
            'current_page': current_page,
            'course_org': course_org,
            'has_fav': has_fav,
        })

class AddFavView(LoginRequiredMixin,View):
    # 用户收藏、取消收藏 课程机构
    def set_fav_nums(self,fav_type,fav_id,num=1):
        if fav_type == 1:
            course = Course.objects.get(id=fav_id)
            course.fav_nums += num
            course.save()
        elif fav_type == 2:
            course_org = CourseOrg.objects.get(id=fav_id)
            course_org.fav_nums += num
            course_org.save()
        elif fav_type == 3:
            teacher = Teacher.objects.get(id=fav_id)
            teacher.fav_nums += num
            teacher.save()
    def post(self,request):
        fav_id = int(request.POST.get('fav_id',0))
        fav_type = int(request.POST.get('fav_type',0))

        res = dict()
        #判断用户是否登陆
        if not request.user.is_authenticated():
            res['status'] = 'fail'
            res['msg'] = '用户未登录'
            return HttpResponse(json.dumps(res),content_type='application/json')
        #查询收藏记录
        exist_records = UserFavorite.objects.filter(user=request.user,fav_id=fav_id, fav_type=fav_type)
        if exist_records:
            exist_records.delete()
            self.set_fav_nums(fav_type,fav_id,-1)
            res['status'] = 'success'
            res['msg'] = '收藏'
        else:
            user_fav = UserFavorite()
            if fav_id and fav_type:
                user_fav.user = request.user
                user_fav.fav_id = fav_id
                user_fav.fav_type = fav_type
                user_fav.save()
                self.set_fav_nums(fav_type,fav_id,1)
                res['status'] = 'success'
                res['msg'] = '已收藏'
            else:
                res['status'] = 'fail'
                res['msg'] = '收藏出错'

        return HttpResponse(json.dumps(res), content_type='application/json')





