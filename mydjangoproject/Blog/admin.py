from django.contrib import admin
from .models import Mark, Post, Student, Subject
# Register your models here.
admin.site.register(Post)
admin.site.register(Student)
admin.site.register(Subject)
admin.site.register(Mark)
