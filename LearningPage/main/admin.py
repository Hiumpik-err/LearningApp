# accounts/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Uzytkownik, Article, Course, Quizz
from .forms import UzytkownikCreationForm, UzytkownikChangeForm

class UzytkownikAdmin(UserAdmin):
    form = UzytkownikChangeForm
    add_form = UzytkownikCreationForm

    filter_horizontal = () 

    list_display = ('email', 'is_admin', 'is_active')
    list_filter = ('is_admin', 'is_active', 'groups', 'user_permissions') 
    fieldsets = (
        (None, {'fields': ('email', 'password', 'first_name', 'last_name', 'username', "collected_points", "daily_points", "weekly_points", "profile_image")}),
        ('Permissions', {'fields': ('is_admin', 'is_active', 'is_superuser', 'groups', 'user_permissions')}), 
        ('Important dates', {'fields': ('last_login',)}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password', 'password2', "collected_points"), 
        }),
    )
    
    search_fields = ('email',)
    ordering = ('email',)
    readonly_fields = ('last_login',)

admin.site.register(Uzytkownik, UzytkownikAdmin)
admin.site.register(Article)
admin.site.register(Course)
admin.site.register(Quizz)