from django.db import models


# Create your models here.
#
class Users(models.Model):
    iros2020_name = models.CharField(max_length=100)
    iros2020_email = models.CharField(max_length=100)

    def __str__(self):
        return f"iros2020_name:{self.iros2020_name}, iros2020_email:{self.iros2020_email}"

class Papers(models.Model):
    #IROS Registered Paper ID
    paper_id = models.PositiveIntegerField(default=0, null=True)
    #Users that clicked likes
    like_users = models.ManyToManyField(Users, blank=True, related_name='like_papers')

    def __str__(self):
        return f"paper_id:{self.paper_id}"


# class Likes(models.Model):
#     paper_id = models.PositiveIntegerField()
#     memberEmail = models.CharField(max_length=140)


# class Comments(models.Model):
#     paper_id = models.PositiveIntegerField()
#     name = models.CharField(max_length=140)
#     member = models.CharField(max_length=140)
#     comment = models.CharField(max_length=140)