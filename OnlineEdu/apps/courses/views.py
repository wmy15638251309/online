from django.shortcuts import render,HttpResponse
from django.views.generic.base import View
import  json
from utils.mixin_utils import LoginRequiredMixin
# Create your views here.
from courses.models import Course, CourseResource, Video
from django.db.models import Q
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from operation.models import UserFavorite, UserCourse, CourseComments
from organization.models import Teacher, CourseOrg


class CourseListView(View):
    def get(self,request):
        #获取课程
        all_courses = Course.objects.all().order_by('-add_time')
        #获取热门的课程
        hot_courses = Course.objects.all().order_by('-click_nums')
        #课程搜索
        search_keywords = request.GET.get('keywords','')
        if search_keywords:
            all_courses = all_courses.filter(
                Q(name__icontains=search_keywords)|
                Q(desc__icontains=search_keywords) |
                Q(detail__icontains=search_keywords)
            )
        #课程排序
        sort = request.GET.get('sort','')
        if sort == 'students':
            all_courses = all_courses.order_by('-students')
        elif sort == 'hot':
            all_courses = all_courses.order_by('-click_nums')
            # 对课程进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_courses, 3, request=request)
        courses = p.page(page)

        return render(request, 'course-list.html', {
            'all_courses': courses,
            'hot_courses': hot_courses,
            'sort': sort,
        })



# 课程详情
class CourseDetailView(View):
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id)) #和数据库打交道的
        # 课程点击数 + 1
        course.click_nums += 1
        course.save()
        # 找到相关课程
        tag = course.tag
        relate_courses = []
        if tag:
            relate_courses = Course.objects.filter(tag=tag)[:2]

        # 课程/机构收藏
        has_fav_course = False
        has_fav_org = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course.id, fav_type=1):
                has_fav_course = True
            if UserFavorite.objects.filter(user=request.user, fav_id=course.course_org.id, fav_type=2):
                has_fav_org = True

        return render(request, 'course-detail.html', {
            'course': course,
            'relate_courses': relate_courses,
            'has_fav_course': has_fav_course,
            'has_fav_org': has_fav_org,
        })


# 课程信息
class CourseInfoView( LoginRequiredMixin,View):
    def get(self,request,course_id):
        course = Course.objects.get(id=int(course_id))
        course.students += 1
        course.save()
        #查看是否学习
        user_courses = UserCourse.objects.filter(user=request.user,course=course)
        if not user_courses:
            user_courses = UserCourse(user=request.user, course=course)
            user_courses.save()
        #学过的课程
        user_courses = UserCourse.objects.filter(course=course)
        #根据课程查找所有用户
        user_ids = [user_course.user.id for user_course in user_courses]
        #根据用户id查找所有的课程
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        #找找用户对应的课程
        course_ids = [user_course.course.id for user_course in all_user_courses]
        relate_courses = Course.objects.filter(id__in=course_ids).order_by('-click_nums')[:3]
        all_resources = CourseResource.objects.filter(course=course)
        return render(request, 'course-video.html', {
            'course': course,
            'all_resources': all_resources,
            'relate_courses': relate_courses,
        })

'''评论逻辑'''
class CommentView(LoginRequiredMixin,View):
    def get(self,request,course_id):
        course = Course.objects.get(id=int(course_id))
        #资源下载
        all_resources = CourseResource.objects.filter( course=course)
        #课程的所有评论
        all_comments = CourseComments.objects.filter(course=course)
        # 得出学过该课程的同学还学过的课程
        user_courses = UserCourse.objects.filter(course=course)
        # 根据课程查找所有用户
        user_ids = [user_course.user.id for user_course in user_courses]
        # 根据用户id查找所有的课程
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        # 找找用户对应的课程
        course_ids = [user_course.course.id for user_course in all_user_courses]
        relate_courses = Course.objects.filter(id__in=course_ids).order_by('-click_nums')[:3]
        return render(request, 'course-comment.html', {
            'course': course,
            'all_resources': all_resources,
            'all_comments': all_comments,
            'relate_courses': relate_courses,
        })

'''添加评论信息逻辑'''
class AddCommentView(LoginRequiredMixin,View):
    def post(self,request):
        #判断用户状态
        res =dict()
        if not request.user.is_authenticated():
            res['status'] = 'fail'
            res['msg'] = '用户未登录'
            return HttpResponse(json.dumps(res), content_type='application/json')
        course_id = int(request.POST.get('course_id',0))
        comments = request.POST.get('comments','')

        if course_id and comments:
            course_comments = CourseComments()
            course_comments.course = Course.objects.get(id=course_id)
            course_comments.comments = comments
            course_comments.user = request.user
            course_comments.save()
            res['status'] = 'success'
            res['msg'] = '添加成功'
        else:
            res['status'] = 'fail'
            res['msg'] = '添加失败'

        return HttpResponse(json.dumps(res), content_type='application/json')

'''视频播放'''
class VideoPlayView(LoginRequiredMixin,View):
    def get(self, request, video_id):
        video = Video.objects.get(id=int(video_id))
        course = video.lesson.course
        course.students += 1
        course.save()
        # 查询用户是否学习该课程
        user_couses = UserCourse.objects.filter(user=request.user, course=course)
        if not user_couses:
            user_couses = UserCourse(user=request.user,course=course)
            user_couses.save()

        #所有用户的id
        user_couseses = UserCourse.objects.filter(course=course)
        user_ids =  [user_couse.user.id for user_couse in user_couseses]
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        course_ids = [ user_couse.course.id for user_couse in  all_user_courses]
        relate_courses =  Course.objects.filter(id__in=course_ids).order_by('-click_nums')[:3]
         #查询所有的资源
        all_resources = CourseResource.objects.filter(course=course)

        return  render(request,'video-play.html',{
            'course':course,
            'relate_courses':relate_courses,
            'all_resources':all_resources,
            'video': video,
        })


'''讲师列表页'''
class TeacherListView(View):
    def get(self,request):
        #获取讲师
        all_teachers = Teacher.objects.all().order_by('add_time')
        hot_teachers = Teacher.objects.all().order_by('-work_years')
        tea_num = Teacher.objects.all().count()
        #讲师搜索
        search_keywords = request.GET.get('keywords','')
        if search_keywords:
            all_teachers = all_teachers.filter(
                Q(name__icontains=search_keywords) |
                Q(work_company__icontains=search_keywords) |
                Q(tag__icontains=search_keywords) |
                Q(points__icontains=search_keywords)
            )
        #课程排序
        sort = request.GET.get('sort','')
        if sort == 'hot':
            all_teachers = all_teachers.order_by('-click_nums')
            # 对讲师进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_teachers, 1, request=request)
        teachers = p.page(page)

        return render(request, 'teachers-list.html', {
            'hot_teachers':hot_teachers,
            'tea_num':tea_num,
            'all_teachers': teachers,
            'sort': sort,
        })

class TeacherDetailView(View):
    def get(self,request,teacher_id):
        #获取讲师
        teacher = Teacher.objects.get(id=int(teacher_id))
        #根据教师找课程
        teacher_course = teacher.course_set.all()
        # teacher_course = CourseOrg.objects.filter(teacher=teacher)
        # 根据教师找机构
        teacher_org = teacher.org
        all_teachers = Teacher.objects.all().order_by('add_time')
        hot_teachers = Teacher.objects.all().order_by('-work_years')
        tea_num = Teacher.objects.all().count()
        #讲师搜索
        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            all_teachers = all_teachers.filter(
                Q(name__icontains=search_keywords) |
                Q(work_company__icontains=search_keywords) |
                Q(work_position__icontains=search_keywords)
            )
        #课程排序
        sort = request.GET.get('sort','')
        if sort == 'hot':
            all_teachers = all_teachers.order_by('-click_nums')
            # 对讲师进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(teacher_course, 1, request=request)
        coursers = p.page(page)

        has_fav_teacher = False
        has_fav_org = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=teacher.id, fav_type=1):
                has_fav_teacher = True
            if UserFavorite.objects.filter(user=request.user, fav_id=teacher.org.id, fav_type=2):
                has_fav_org = True

        return render(request, 'teacher-detail.html', {
            'hot_teachers':hot_teachers,
            'tea_num':tea_num,
            'all_teachers': all_teachers,
            'sort': sort,
            'has_fav_teacher':has_fav_teacher,
            'has_fav_org':has_fav_org,
            'teacher_course':coursers,
            'teacher_org':teacher_org,
            'teacher':teacher,
        })




