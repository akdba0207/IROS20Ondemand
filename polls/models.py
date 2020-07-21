from django.db import models


# Create your models here.

class Like(models.Model):
    name = models.CharField(max_length=100)
    paper_id = models.CharField(max_length=100)

    def __str__(self):
        return f"name: {self.name}, paper_id: {self.paper_id}"



