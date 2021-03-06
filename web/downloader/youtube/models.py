from django.db import models


class UserRequests(models.Model):
    url = models.URLField()
    download_url = models.TextField()
    email = models.EmailField()
    title = models.CharField(max_length=300, blank=True)
    size = models.IntegerField(null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    media = models.FileField(upload_to='uploads/', null=True)

    def __strt__(self):
        return (self.email, self.title)
