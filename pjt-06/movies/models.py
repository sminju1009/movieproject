from django.db import models
from django.conf import settings

# Create your models here.
class Movie(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=20)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # 장르 선택
    COMEDY = 'Comedy'
    FANTASY = 'Fantasy'
    ROMANCE = 'Romance'
    GENRE_CHOICES = [
        (COMEDY, 'Comedy'),
        (FANTASY, 'Fantasy'),
        (ROMANCE, 'Romance'),
    ]
    genre = models.CharField(
        max_length = 7,
        choices = GENRE_CHOICES,
        default = COMEDY,
    )
    # 평점 입력받기
    rating = models.DecimalField(
        max_digits=2,  # 정수부 자릿수, 5까지 허용하므로 2로 설정
        decimal_places=1,  # 소수부 자릿수, 0.5 간격이므로 1로 설정
        default=0.0,  # 기본값 설정
    )
    # 좋아요 기능 구현
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_movies')


class Comment(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Recomment(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    content = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)