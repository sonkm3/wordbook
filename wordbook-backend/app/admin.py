from django.contrib import admin

from .models import Word, Course, Student, CustomUser


admin.site.register(Word)


admin.site.register(Course)


admin.site.register(Student)


admin.site.register(CustomUser)
