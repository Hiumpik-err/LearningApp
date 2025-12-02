# accounts/forms.py
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Uzytkownik, Article, Course, Quizz
from django import forms
from tinymce.widgets import TinyMCE
from django.core.validators import RegexValidator

EMAIL_REGEX = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$'  
email_validation = RegexValidator(
    regex=EMAIL_REGEX,
    message="Enter valid email",
    code="invalid_strict_email"
)

PASSWORD_REGEX = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()\-+_=])(?=.{8,}).*$'
password_validation = RegexValidator(
    regex=PASSWORD_REGEX,
    message="Enter more complex password",
    code="invalid_password"
)

CATEGORY_CHOICES = [
        ('', '---Choose category---'),
        ('Math', 'Math'),
        ('Physics', 'Physics'),
        ('Chemistry', 'Chemistry'),
        ('Biology', 'Biology'),
        ('History', 'History'),
        ('English', 'English'),
    ]

class UzytkownikForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'required': True, 
        'class' : 'form-control',
        'id' : 'input-password',
        'placeholder' : 'Enter your password'
        # 'title' : "Password must contain the following 1 Uppercase letter 1 Lowercase letter 1 Special character Must be at least 8 characters"
        }),
        validators=[password_validation])
    email = forms.EmailField(
        validators=[email_validation], 
        widget=forms.EmailInput(attrs={
            'required': True, 
            'class' : 'form-control',
            'placeholder' : 'Enter your email'
        })
    )
    class Meta:
        model = Uzytkownik
        fields = ["email", "password"]

class UzytkownikCreationForm(UserCreationForm):
    class Meta:
        model = Uzytkownik
        fields = ('email',) 

class UzytkownikChangeForm(UserChangeForm):
    class Meta:
        model = Uzytkownik
        fields = ('email', 'is_active', 'is_admin')


class ArticleForm(forms.ModelForm):
    
    category = forms.ChoiceField(
        choices=CATEGORY_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-select text-center',
            'required': True
        })
    )
    
    class Meta:
        model = Article
        fields = ['category', 'title', 'lead', 'content']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Title',
                'required': True,
                'minlength': 3,
                'maxlength': 200
            }),
            'lead': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Lead',
                'required': True,
                'minlength': 3,
                'maxlength': 200
            }),
            'content': TinyMCE(attrs={
                'cols': 80,
                'rows': 30,
                'required': True,
                'minlength': 10
            })
        }
        
    def clean_title(self):
        title = self.cleaned_data.get('title')
        if len(title) < 3:
            raise forms.ValidationError('Title must be at least 3 characters long.')
        if len(title) > 200:
            raise forms.ValidationError('Title must be no more than 200 characters long.')
        return title
        
    def clean_category(self):
        category = self.cleaned_data.get('category')
        if not category:
            raise forms.ValidationError('Please select a category.')
        return category
        
    def clean_content(self):
        content = self.cleaned_data.get('content')
        if content and len(content.strip()) < 10:
            raise forms.ValidationError('Content must be at least 10 characters long.')
        return content


class CourseForm(forms.ModelForm):
    
    category = forms.ChoiceField(
        choices=CATEGORY_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-select text-center',
            'required': True
        })
    )
    
    class Meta:
        model = Course
        fields = ['category', 'title', 'question', 'answers']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Title',
                'required': True,
                'minlength': 3,
                'maxlength': 200
            }),
            'question': forms.Textarea(attrs={
                'class': 'form-control form-textarea',
                'placeholder': 'Question',
                'required': True,
                'minlength': 10
            }),
            'answers': forms.Textarea(attrs={
                'class': 'form-control form-textarea',
                'placeholder': 'Possible answers separated by semicolon'
            })
        }


class QuizzForm(forms.ModelForm):
    # CATEGORY_CHOICES = [
    #     ('', '---Choose category---'),
    #     ('Math', 'Math'),
    #     ('Physics', 'Physics'),
    #     ('Chemistry', 'Chemistry'),
    #     ('Biology', 'Biology'),
    #     ('History', 'History'),
    #     ('English', 'English'),
    # ]
    
    category = forms.ChoiceField(
        choices=CATEGORY_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-select text-center',
            'required': True
        })
    )
    
    class Meta:
        model = Quizz
        fields = ['category', 'title', 'description', 'link']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Title',
                'required': True,
                'minlength': 3,
                'maxlength': 200
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control form-textarea',
                'placeholder': 'Description',
                'required': True,
                'minlength': 10
            }),
            'link': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://example.com',
                'required': True
            })
        }        