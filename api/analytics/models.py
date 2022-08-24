from django.db import models


class Analytic(models.Model):
    anonymous_id = models.CharField(max_length=50, null=True)
    title = models.CharField(max_length=50, null=True)
    event = models.CharField(max_length=50,  null=True)
    channel = models.CharField(max_length=10,  null=True)
    category = models.CharField(max_length=10,  null=True)
    resource = models.CharField(max_length=50,  null=True)
    url = models.CharField(max_length=50,  null=True)
    path = models.CharField(max_length=50,  null=True)
    user_id = models.CharField(max_length=50,  null=True)
    method = models.CharField(max_length=20,  null=True)
    response_time = models.CharField(max_length=10,  null=True)
    day = models.CharField(max_length=10,  null=True)
    hour = models.CharField(max_length=10,  null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.title
