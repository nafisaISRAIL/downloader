from django.db import models


# Create your models here.
class UserRequests(models.Model):
    url = models.URLField()
    title = models.CharField(max_length=300, blank=True)
    size = models.IntegerField()
    created_date = models.DateTimeField(auto_now_add=True)
