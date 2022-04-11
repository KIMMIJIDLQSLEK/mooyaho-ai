from django.db import models
from django import forms
# Create your models here.
from userpost.models import MooyahoUser,Post,Mountain


class UserViewLog(models.Model):
    class Meta:
        db_table = "userviewlog"

    user = models.ForeignKey(MooyahoUser, on_delete=models.CASCADE)
    post_mountain_id = models.IntegerField(null=True, blank=True)
    mountain = models.ForeignKey(Mountain, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # 각 객체가 유저 닉네임, 본 산으로 표시되도록 설정
    def __str__(self):
        user_name = self.user.nickname
        user_saw_mountain = self.mountain.mountain_name
        return user_name + ' / ' + user_saw_mountain

