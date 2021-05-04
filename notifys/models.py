from django.db import models


# Create your models here.
class Notify(models.Model):
    title = models.CharField(max_length=256)
    content = models.TextField()
    pub_date = models.DateField()
