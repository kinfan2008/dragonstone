from django.contrib import admin
from dragon.models import UserProfile,Experiment,ApplyRecord

admin.site.register(UserProfile)
admin.site.register(Experiment)
admin.site.register(ApplyRecord)