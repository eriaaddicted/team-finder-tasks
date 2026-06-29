from django.db import models
from django.conf import settings

class Project(models.Model):
    STATUS_CHOICES = (('open', 'Открыт'), ('closed', 'Закрыт'))
    
    title = models.CharField(max_length=255, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    github_url = models.URLField(blank=True, null=True, verbose_name="GitHub")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='open')
    
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='projects')
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='participated_projects', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']