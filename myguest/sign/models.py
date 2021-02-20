from django.db import models

# Create your models here.
#发布会表
class Event(models.Model):
    name1=models.CharField(max_length=100) #发布会标题
    limit1=models.IntegerField()#参加人数
    status1=models.BooleanField()#状态
    address1=models.CharField(max_length=200)#地址
    start_time1=models.DateTimeField('events_time')#发布会时间
    create_time1=models.DateTimeField(auto_now=True)#创建时间

    def __str__(self):
        return self.name1

class Guest(models.Model):
    event=models.ForeignKey(Event,on_delete=models.CASCADE)#关联发布会id（外键）
    realname=models.CharField(max_length=64)#姓名
    phone=models.CharField(max_length=16)#手机号
    email=models.EmailField()#邮箱
    sign=models.BooleanField()#签到状态
    create_time=models.DateTimeField(auto_now=True)#创建时间

class Meta:
      unique_together=("event","phone")

      def __str__(self):
          return self.realname

