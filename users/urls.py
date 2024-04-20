from django.urls import path
from users.views import RegisterView,LoginView,LogoutView,ForgetPasswordView,UserCenterView,WriteBlogView

urlpatterns = [
    # path的第一个参数： 路由
    # path的第二个参数： 视图函数名
    path('register/',RegisterView.as_view(),name='register'),

    #登录路由
    path('login/',LoginView.as_view(),name='login'),

    # 退出登录
    path('logout/', LogoutView.as_view(), name='logout'),

    # 忘记密码
    path('forgetpassword/', ForgetPasswordView.as_view(), name='forgetpassword'),

    # 个人中心
    path('center/',UserCenterView.as_view(),name='center'),

    # 写博客的路由
    path('writeblog/', WriteBlogView.as_view(), name='writeblog'),
]