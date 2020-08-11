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

    #Users that clicked save
    save_users = models.ManyToManyField(Users, blank=True, related_name='save_papers')

    def __str__(self):
        return f"paper_id:{self.paper_id}"

class Comments(models.Model):
    paper_id = models.PositiveIntegerField(default=0, null=True)
    comment = models.TextField(max_length=1500)
    comment_users = models.ManyToManyField(Users, blank=True, related_name='comment_papers')

# class SavePapers(models.Model):
#     #IROS Registered Paper ID
#     paper_id = models.PositiveIntegerField(default=0, null=True)
#     #Users that clicked likes
#     save_users = models.ManyToManyField(Users, blank=True, related_name='save_papers')
#
#     def __str__(self):
#         return f"paper_id:{self.paper_id}"