from .models import Task, Uzytkownik, Article
from django.forms import ModelForm

class ArticleForm(ModelForm):
    class Meta:
        model = Article
        fields = ["topic", "subject", "description"]

class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ["topic", "subject", "description", "answer"]