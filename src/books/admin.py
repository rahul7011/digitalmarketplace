from django.contrib import admin
from .models import Author,Book,Exercise,Chapter,Solution,UserLibrary

# Register your models here.
admin.site.register(UserLibrary)
admin.site.register(Author)
admin.site.register(Book)
admin.site.register(Chapter)
admin.site.register(Exercise)
admin.site.register(Solution)
