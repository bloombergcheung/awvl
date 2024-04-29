from django.urls import path
from users.views import RegisterView,LoginView,LogoutView,ForgetPasswordView,UserCenterView,WriteBlogView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/',RegisterView.as_view(),name='register'),

    path('login/',LoginView.as_view(),name='login'),

    path('logout/', LogoutView.as_view(), name='logout'),

    path('forgetpassword/', ForgetPasswordView.as_view(), name='forgetpassword'),

    path('center/',UserCenterView.as_view(),name='center'),

    path('writeblog/', WriteBlogView.as_view(), name='writeblog'),
]