from django.contrib import admin

# Register your models here.
from django.contrib import admin
from app import models

admin.site.register(models.Profile)
admin.site.register(models.Question)
admin.site.register(models.Answer)
admin.site.register(models.LikeAnswer)
admin.site.register(models.LikeQuestion)
admin.site.register(models.Tag)