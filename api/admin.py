from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import *
import nested_admin


class StatisticsAdmin(admin.TabularInline):
    model = Statistics


class ProfileAdmin(admin.TabularInline):
    model = Profile


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ("first_name", 'last_name', 'email', "created_at", "updated_at")
    list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('first_name', "last_name", 'email', 'password',)}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
         ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    inlines = (ProfileAdmin, StatisticsAdmin)


admin.site.register(CustomUser, CustomUserAdmin)


class CommentAdmin(nested_admin.NestedTabularInline):
    model = Comment


class AnswerAdmin(nested_admin.NestedTabularInline):
    model = Answer


class TaskAdmin(nested_admin.NestedTabularInline):
    model = Task
    inlines = [AnswerAdmin, ]


@admin.register(Exam)
class ExamAdmin(nested_admin.NestedModelAdmin):
    list_display = ("author", "title", "is_show", "publish_time")
    list_filter = ("is_show", "publish_time",)
    search_fields = ("title",)
    ordering = ("publish_time",)
    inlines = [TaskAdmin, CommentAdmin, ]
