from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from tinymce.models import HTMLField


class UzytkownikManager(BaseUserManager):
    def create_user(self, email, password = None):
        if not email:
            raise ValueError("Email must be provided")

        user = self.model(
            email = self.normalize_email(email)
        )
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, email, password):
        user = self.create_user(
            email = email,
            password = password 
        )
        user.is_superuser = True
        user.is_admin = True
        user.save(using=self._db)
        return user
    
class Uzytkownik(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=50, unique=True, null=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [] 

    objects = UzytkownikManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
    

class Article(models.Model):
    
    ArticleId = models.BigAutoField(primary_key=True)
    title = models.CharField(null=False, max_length=255)
    lead = models.CharField(null=False, max_length=255)
    content = HTMLField(null=True)
    category = models.CharField(null=False, max_length=50)

    def __str__(self):
        return self.title
    
class Quizz(models.Model):
    QuizzId = models.BigAutoField(primary_key=True)
    title = models.CharField(null=False, max_length=255)
    description = models.CharField(null=False, max_length=500)
    link = models.URLField(max_length=200, null=False)
    category = models.CharField(max_length=50, null=False)

    def __str__(self):
        return self.title
    
class Course(models.Model):
    CourseId = models.BigAutoField(primary_key=True)
    category = models.CharField(max_length=50, null=False)
    title = models.CharField(null=False, max_length=255)
    question = models.TextField(null=False)
    answers = models.CharField(max_length=255)

    def __str__(self):
        return self.title