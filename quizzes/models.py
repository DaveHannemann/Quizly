from django.db import models

# Create your models here.
class Quiz(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    video_url = models.URLField()
    questions = models.JSONField()
    created_by = models.ForeignKey('auth.User', on_delete=models.CASCADE)
