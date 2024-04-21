from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):

    email_address = models.CharField(max_length=20, blank=False)

    avatar = models.ImageField(upload_to='avatar/%Y%m%d/', blank=True)

    user_desc = models.CharField(max_length=500, blank=True)

    full_name = models.CharField(max_length=20, blank=True)

    username = models.CharField(max_length=20, unique=True, blank=True)

    OS_type = models.CharField(max_length=500, blank=True)

    IP_address = models.CharField(max_length=500, blank=True)

    Team = models.CharField(max_length=500, blank=True)

    Role = models.CharField(max_length=500, blank=True)

    Team_name = models.CharField(max_length=500, blank=True)

    Team_task = models.CharField(max_length=500, blank=True)



    # 修改认证的字段为
    USERNAME_FIELD: str = 'username'

    class Meta:
        db_table='tb_users'  #修改表名
        verbose_name='用户管理' #admin 后台显示
        verbose_name_plural=verbose_name #admin后台显示

    def __str__(self):
        return self.username