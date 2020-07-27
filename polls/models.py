from django.db import models


# Create your models here.

class Like(models.Model):
    name = models.CharField(max_length=100)
    paper_id = models.CharField(max_length=100)

    def __str__(self):
        return f"name: {self.name}, paper_id: {self.paper_id}"

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
