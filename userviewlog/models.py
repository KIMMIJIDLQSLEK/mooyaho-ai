from django.db import models


# Create your models here.
from userpost.models import MooyahoUser,Post
    # Mountain


class UserViewLog(models.Model):
    class Meta:
        db_table = "userviewlog"

        user_id = models.ForeignKey(MooyahoUser, on_delete=models.CASCADE, unique=False)
        post_id = models.ForeignKey(Post, on_delete=models.CASCADE, unique=False)
        # mountain_id= models.ForeignKey(Mountain, on_delete=models.CASCADE, unique=False)
        created_at = models.DateTimeField(auto_now_add=True)