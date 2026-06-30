from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

from constants import MAX_LENGTH_SKILL_NAME, MAX_LENGTH_USER_NAME, MAX_LENGTH_USER_PHONE


class UserManager(BaseUserManager):
    """Кастомный менеджер для модели пользователя, где email является уникальным идентификатором."""
    
    def create_user(self, email, name, surname, password=None, **extra_fields):
        if not email:
            raise ValueError('Поле Email должно быть заполнено')
        email = self.normalize_email(email)
        extra_fields.setdefault('is_active', True)
        user = self.model(email=email, name=name, surname=surname, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, surname, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Суперпользователь должен иметь is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Суперпользователь должен иметь is_superuser=True.')

        return self.create_user(email, name, surname, password, **extra_fields)


class Skill(models.Model):
    name = models.CharField(
        max_length=MAX_LENGTH_SKILL_NAME, 
        unique=True, 
        verbose_name="Название навыка"
    )

    class Meta:
        verbose_name = "Навек"
        verbose_name_plural = "Навыки"
        ordering = ["name"]

    def __str__(self):
        return self.name


class User(AbstractUser):
    
    username = None 
    
    email = models.EmailField(unique=True, verbose_name="Email")
    name = models.CharField(max_length=MAX_LENGTH_USER_NAME, verbose_name="Имя")
    surname = models.CharField(max_length=MAX_LENGTH_USER_NAME, verbose_name="Фамилия")
    
    about = models.TextField(blank=True, default="", verbose_name="О себе")
    phone = models.CharField(max_length=MAX_LENGTH_USER_PHONE, blank=True, default="", verbose_name="Телефон")
    github_url = models.URLField(blank=True, default="", verbose_name="GitHub")
    
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name="Аватар")
    
    skills = models.ManyToManyField(Skill, related_name='users', blank=True, verbose_name="Навыки")

    
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'surname']

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ["-date_joined"]

    def __str__(self):
        return f"{self.name} {self.surname} ({self.email})"