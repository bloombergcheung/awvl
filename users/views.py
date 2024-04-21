# Create your views here.
from django.shortcuts import render
from django.views import View
from django.http.response import HttpResponseBadRequest
from users.models import User
from django.db import DatabaseError
from django.shortcuts import  redirect
from django.urls import reverse
import re

#注册视图
class RegisterView(View):
    def get(self,request):

        return render(request,'register.html')

    def post(self,request):

        # 1.接收数据
        username = request.POST.get('username')
        email_address = request.POST.get('email_address')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        full_name = request.POST.get('full_name')
        OS_type = request.POST.get('OS_type')
        IP_address = request.POST.get('IP_address')
        Team = request.POST.get('Team')
        Role = request.POST.get('Role')
        Team_name = request.POST.get('Team_name')

        # 2.验证数据
        #     2.1 参数是否齐全
        if not all([email_address,password,password2]):
            return HttpResponseBadRequest('缺少必要的参数')
        #     2.4 密码和确认密码要一致
        if password != password2:
            return HttpResponseBadRequest('两次密码不一致')
        # 3.保存注册信息
        # create_user 可以使用系统的方法来对密码进行加密
        try:
            user=User.objects.create_user(username=username,
                                      email=email_address,
                                      email_address=email_address,
                                      password=password,
                                      full_name=full_name,
                                      OS_type=OS_type,
                                      IP_address=IP_address,
                                      Team=Team,
                                      Role=Role,
                                      Team_name=Team_name,
                                          )
        except DatabaseError as e:
            logger.error(e)
            return HttpResponseBadRequest('注册失败')

        from django.contrib.auth import login
        login(request,user)
        # 4.返回响应跳转到指定页面
        # 暂时返回一个注册成功的信息，后期再实现跳转到指定页面

        # redirect 是进行重定向
        # reverse 是可以通过 namespace:name 来获取到视图所对应的路由
        response = redirect(reverse('home:index'))
        # return HttpResponse('注册成功，重定向到首页')

        #设置cookie信息，以方便首页中 用户信息展示的判断和用户信息的展示
        response.set_cookie('is_login',True)
        response.set_cookie('username',user.username,max_age=7*24*3600)

        return response



from django.http.response import JsonResponse
import logging
logger=logging.getLogger('django')


class LoginView(View):

    def get(self,request):

        return render(request,'login.html')
    def post(self,request):

        # 1.接收参数
        username=request.POST.get('username')
        password=request.POST.get('password')
        remember=request.POST.get('remember')
        # 2.参数的验证
        #     2.2 验证密码是否符合规则
        if not re.match(r'^[a-zA-Z0-9]{8,20}$',password):
            return HttpResponseBadRequest('密码不符合规则')
        # 3.用户认证登录
        # 采用系统自带的认证方法进行认证
        # 如果我们的用户名和密码正确，会返回user
        # 如果我们的用户名或密码不正确，会返回None
        from django.contrib.auth import authenticate
        # 默认的认证方法是 针对于 username 字段进行用户名的判断
        # 我们需要到User模型中进行修改，等测试出现问题的时候，我们再修改
        user=authenticate(username=username,password=password)

        if user is None:
            return HttpResponseBadRequest('用户名或密码错误')
        # 4.状态的保持
        from django.contrib.auth import login
        login(request,user)
        # 5.根据用户选择的是否记住登录状态来进行判断
        # 6.为了首页显示我们需要设置一些cookie信息
        # 根据next参数来进行页面的跳转
        next_page = request.GET.get('next')
        if next_page:
            response = redirect(next_page)
        else:
            response = redirect(reverse('home:index'))


        if remember != 'on':  #没有记住用户信息
            #浏览器关闭之后
            request.session.set_expiry(0)
            response.set_cookie('is_login',True)
            response.set_cookie('username',user.username,max_age=14*24*3600)
        else:                 # 记住用户信息
            # 默认是记住 2周
            request.session.set_expiry(None)
            response.set_cookie('is_login',True,max_age=14*24*3600)
            response.set_cookie('username',user.username,max_age=14*24*3600)

        # 7.返回响应
        return response

from django.contrib.auth import logout
class LogoutView(View):

    def get(self,request):
        # 1.session数据清除
        logout(request)
        # 2.删除部分cookie数据
        response=redirect(reverse('home:index'))
        response.delete_cookie('is_login')
        #3.跳转到首页
        return response



class ForgetPasswordView(View):

    def get(self,request):

        return render(request,'forget_password.html')

    def post(self, request):

        email_address = request.POST.get('email_address')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        full_name = request.POST.get('full_name')
        OS_type = request.POST.get('OS_type')
        IP_address = request.POST.get('IP_address')
        Team = request.POST.get('Team')
        Role = request.POST.get('Role')
        Team_name = request.POST.get('Team_name')

        if not all([email_address, password, password2]):
            return HttpResponseBadRequest('参数不全')
        if not re.match(r'^[0-9A-Za-z]{8,20}$', password):
            return HttpResponseBadRequest('密码不符合格则')
        if password2 != password:
            return HttpResponseBadRequest('密码不一致')
            # 3.根据手机号进行用户信息的查询
        try:
            user = User.objects.get(email_address=email_address)
        except User.DoesNotExist:
            # 5.如果手机号没有查询出用户信息，则进行新用户的创建
            try:
                User.objects.create_user(username=email_address,
                                                email_address=email_address,
                                                email=email_address,
                                                password=password,
                                                full_name=full_name,
                                                OS_type=OS_type,
                                                IP_address=IP_address,
                                                Team=Team,
                                                Role=Role,
                                                Team_name=Team_name,
                                                )
            except Exception:
                return HttpResponseBadRequest('修改失败，请稍后再试')
        else:
            # 4.如果手机号查询出用户信息则进行用户密码的修改
            user.set_password(password)
            # 注意，保存用户信息
            user.save()
            # 6.进行页面跳转，跳转到登录页面
        response = redirect(reverse('users:login'))
            # 7.返回响应
        return response


from django.contrib.auth.mixins import LoginRequiredMixin
# 如果用户未登录的话，则会进行默认的跳转
# 默认的跳转连接是：accounts/login/?next=xxx
class UserCenterView(LoginRequiredMixin,View):

    def get(self,request):
        # 获得登录用户的信息
        user=request.user
        #组织获取用户的信息
        context = {
            'username':user.username,
            'email_address':user.email_address,
            'avatar':user.avatar.url if user.avatar else None,
            'user_desc':user.user_desc,
            'full_name':user.full_name,
            'OS_type':user.OS_type,
            'IP_address':user.IP_address,
            'Team': user.Team,
            'Role': user.Role,
            'Team_name': user.Team_name,
        }
        return render(request,'center.html',context=context)


    def post(self,request):

        user=request.user
        # 1.接收参数
        username = request.POST.get('username',user.username)
        user_desc = request.POST.get('desc',user.user_desc)
        avatar = request.FILES.get('avatar')
        full_name = request.POST.get('full_name')
        OS_type = request.POST.get('OS_type')
        IP_address = request.POST.get('IP_address')
        Team = request.POST.get('Team')
        Role = request.POST.get('Role')
        Team_name = request.POST.get('Team_name')
        # 2.将参数保存起来
        try:
            user.username=username
            user.user_desc=user_desc
            if avatar:
                user.avatar=avatar
            user.full_name = full_name
            user.OS_type = OS_type
            user.IP_address = IP_address
            user.Team = Team
            user.Role = Role
            user.Team_name = Team_name

            user.save()
        except Exception as e:
            logger.error(e)
            return HttpResponseBadRequest('修改失败，请稍后再试')
        # 3.更新cookie中的username信息
        # 4.刷新当前页面（重定向操作）
        response=redirect(reverse('users:center'))
        response.set_cookie('username',user.username,max_age=14*3600*24)

        # 5.返回响应
        return response

from home.models import ArticleCategory, Article


class WriteBlogView(LoginRequiredMixin,View):

    def get(self,request):
        # 查询所有分类模型
        categories = ArticleCategory.objects.all()

        context = {
            'categories': categories
        }
        return render(request, 'write_blog.html', context=context)
    def post(self,request):

        # 1.接收数据
        avatar=request.FILES.get('avatar')
        title=request.POST.get('title')
        category_id=request.POST.get('category')
        tags=request.POST.get('tags')
        sumary=request.POST.get('sumary')
        content=request.POST.get('content')
        user=request.user

        # 2.验证数据
        # 2.1 验证参数是否齐全
        if not all([avatar,title,category_id,sumary,content]):
            return HttpResponseBadRequest('参数不全')
        # 2.2 判断分类id
        try:
            category=ArticleCategory.objects.get(id=category_id)
        except ArticleCategory.DoesNotExist:
            return HttpResponseBadRequest('没有此分类')
        # 3.数据入库
        try:
            article=Article.objects.create(
                author=user,
                avatar=avatar,
                title=title,
                category=category,
                tags=tags,
                sumary=sumary,
                content=content
            )
        except Exception as e:
            logger.error(e)
            return HttpResponseBadRequest('发布失败，请稍后再试')
        # 4.跳转到指定页面（暂时首页）
        return redirect(reverse('home:index'))
