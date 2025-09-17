from django.db import models

class Uzytkownik(models.Model):
    UserId = models.AutoField(primary_key=True, auto_created=True)
    email = models.EmailField(max_length=254, default=None)
    password = models.CharField(max_length=50)
    username = models.CharField(max_length=15)
    fname = models.CharField(max_length=20)
    lname = models.CharField(max_length=20)

    def __str__(self):
        return self.username

class Article(models.Model):
    ArticleId = models.AutoField(primary_key=True, auto_created=True)
    topic = models.CharField(max_length=50)
    subject = models.CharField(max_length=20)
    description = models.JSONField()
    created = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.topic

class Task(models.Model):
    TaskId = models.AutoField(primary_key=True, auto_created=True)
    topic = models.CharField(max_length=50)
    subject = models.CharField(max_length=20)
    description = models.JSONField()
    created = models.DateField(auto_now_add=True)
    answer = models.IntegerField()
    
    def __str__(self):
        return self.topic

'''
class Quizz(models.Model):
    QuizzId = models.AutoField(primary_key=True, auto_created=True)
    topic = models.CharField(max_length=20)
    subject = models.CharField(max_length=20)
    questions_answers = models.JSONField()
    created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.topic
        
'''