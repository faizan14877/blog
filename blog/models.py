from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
# Create your models here.

class Post(models.Model):
    sno = models.AutoField(primary_key=True)
    author = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    content = models.TextField(max_length=10000)
    slug = models.CharField(max_length=100)
    timestamp = models.DateTimeField(blank=True)

    def __str__(self):
        return f"{self.title} by {self.author}"


class BlogComment(models.Model):
    sno = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    comment = models.TextField(max_length=1000)
    timestamp = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.comment[0:3]} by {self.user.username}"