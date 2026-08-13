from django.contrib import admin
from .models import Register, Category, ShortFilm

@admin.register(Register)
class RegisterAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "email", "role")

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "category_name")

@admin.register(ShortFilm)
class ShortFilmAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "category", "duration", "uploaded_at")