from django.db import models


# Create your models here.

class Like(models.Model):
    name = models.CharField(max_length=1553)
    paperid = models.CharField(max_length=1553)
    paperlikenumb = models.CharField(max_length=1553)

    def __str__(self):
        return f"name: {self.name}, paperid: {self.paperid},paperlikenumb: {self.paperlikenumb}"

class ieeeusers(models.Model):
    ieeeusers_id = models.CharField(max_length=100)
    ieeeusers_password = models.CharField(max_length=100)

    def __str__(self):
        return f"ieeeusers_id:{self.ieeeusers_id}, ieeeusers_password:{self.ieeeusers_password}"


class iros2020registered(models.Model):
    iros2020_name = models.CharField(max_length=100)
    iros2020_email = models.CharField(max_length=100)

    def __str__(self):
        return f"iros2020_name:{self.iros2020_name}, iros2020_email:{self.iros2020_email}"
