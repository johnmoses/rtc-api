from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings

class Meeting(models.Model):
    starter = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_meetings'
    )
    name = models.CharField(max_length=225)
    description = models.TextField(blank=True, null=True)
    photo = models.ImageField(default='pic1.jpg')
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(blank=True, null=True)
    scheduled_at = models.DateTimeField(blank=True, null=True)
    started_at = models.DateTimeField(blank=True, null=True)
    ended_at = models.DateTimeField(blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    is_deleted = models.BooleanField(default=False, verbose_name="Is Deleted")
    is_reoccuring = models.BooleanField(default=False, verbose_name="Is Reoccuring")
