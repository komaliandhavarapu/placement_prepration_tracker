from django.contrib import admin

from django.contrib import admin
from .models import Section, PracticeQuestion, Progress, MockTestQuestion

admin.site.register(Section)
admin.site.register(PracticeQuestion)
admin.site.register(Progress)
admin.site.register(MockTestQuestion)

