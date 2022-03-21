from django.db import models
from django import forms
# Create your models here.
from userpost.models import MooyahoUser,Post,Mountain


class UserViewLog(models.Model):
    class Meta:
        db_table = "userviewlog"

    user= models.ForeignKey(MooyahoUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE,null=True,blank=True)
    mountain= models.ForeignKey(Mountain, on_delete=models.CASCADE,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

