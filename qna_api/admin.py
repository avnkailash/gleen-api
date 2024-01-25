from django.contrib import admin
from qna_api import models

admin.site.register(models.UserProfile)
admin.site.register(models.Question)
