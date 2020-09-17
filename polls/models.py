from django.db import models
from django.contrib.auth.models import User

# Create your models here.
#

class accessWSTR(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    accessibility = models.BooleanField(default=False)

class Users(models.Model):
    iros2020_name = models.CharField(max_length=100)
    iros2020_email = models.CharField(max_length=100)

    def __str__(self):
        return f"iros2020_name:{self.iros2020_name}, iros2020_email:{self.iros2020_email}"

class Papers(models.Model):
    #IROS Registered Paper ID
    paper_id = models.PositiveIntegerField(default=0, null=True)

    #Each Paper HitCount
    paper_hitcount = models.PositiveIntegerField(default=0,null=True)

    #Users that clicked likes
    like_users = models.ManyToManyField(User, blank=True, related_name='like_papers')

    #Users that clicked save
    save_users = models.ManyToManyField(User, blank=True, related_name='save_papers')

    def __str__(self):
        return f"paper_id:{self.paper_id}"

class Comments(models.Model):
    paper_id = models.PositiveIntegerField(default=0, null=True)
    comment = models.TextField(max_length=1500)
    comment_users = models.ManyToManyField(User, blank=True, related_name='comment_papers')

class VideoTimers(models.Model):
    paper_id = models.PositiveIntegerField()
    seconds = models.PositiveIntegerField(default=0)