
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

from django.db import models


# 모델 객체 정의
class MooyahoUser(AbstractUser):
    # 모델의 DB 기본 정보
    class Meta:
        db_table = 'mooyaho_user'

    # ('DB에 저장되는 값', 'admin페이지, 폼에서 표시되는 값')
    # 성별 분류값
    gender_conf = [
        ('0', '남'),
        ('1', '여'),
    ]

    # 연령대 분류값
    age_gr_conf = [
        ('0', '10대'),
        ('1', '20대'),
        ('2', '30대'),
        ('3', '40대'),
        ('4', '50대'),
        ('5', '60대'),
        ('6', '70대 이상'),
    ]

    # 등산 경력 분류값
    exp_conf = [
        ('0', '초급'),
        ('1', '중급'),
        ('2', '고급'),
    ]

    # 등산 목적 분류값
    reason_conf = [
        ('0', '친목모임'),
        ('1', '건강관리'),
        ('2', '탐험'),
        ('3', '친환경'),
        ('4', '취미'),
        ('5', '사진'),
    ]

    # 필드
    nickname = models.CharField(max_length=30, unique=True)
    gender = models.CharField(max_length=2, choices=gender_conf)
    age_gr = models.CharField(max_length=2, choices=age_gr_conf)
    disabled = models.BooleanField(default=False)
    superuser = models.BooleanField(default=False)
    # profile_img = models.ImageField(blank=True, upload_to=profile_img_upload_path)
    profile_img = models.ImageField(blank=True, upload_to=f'user/user_upload_images/{nickname}_%Y%m%d')
    exp = models.CharField(max_length=2, choices=exp_conf)
    reason = models.CharField(max_length=2, choices=reason_conf)

    # 각 유저 객체가 유저 아이디로 표시되도록 설정


# 모델 객체 정의
class Post(models.Model):
    # 모델의 DB 기본 정보
    class Meta:
        # 테이블명 설정
        db_table = 'mooyaho_post'

    # 필드
    # hiking_img = models.ImageField(null=False, blank=False, upload_to=hiking_img_upload_path)
    author = models.ForeignKey(MooyahoUser, related_name='mooyaho_user_post', on_delete=models.CASCADE)
    hiking_img = models.ImageField(null=False, blank=False, upload_to=f'post/post_upload_images/{author}%Y%m%d')
    title = models.CharField(max_length=20)
    location = models.CharField(max_length=20)
    content = models.TextField()
    rating = models.SmallIntegerField()
    deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(MooyahoUser, related_name='post_likes')

    # 각 글 객체가 제목으로 표시되도록 설정

class Mountain(models.Model):
    class Meta:
        managed = True
        db_table = 'mountain'

    id = models.BigIntegerField(primary_key=True)
    mountain_id = models.FloatField(blank=True, null=True)
    mountain_name = models.CharField(max_length=30, blank=True, null=True)
    subtitle = models.TextField(blank=True, null=True)
    height = models.IntegerField(blank=True, null=True)
    selection_reason = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=300, blank=True, null=True)
    detail = models.TextField(blank=True, null=True)
    course_information = models.TextField(blank=True, null=True)
    mountain_information = models.TextField(blank=True, null=True)
    stay = models.TextField(blank=True, null=True)
    transportation = models.TextField(blank=True, null=True)
    local_code = models.FloatField(blank=True, null=True)
    local_name = models.TextField(blank=True, null=True)















