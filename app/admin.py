from django.contrib import admin

# Register your models here.
from .models import CustomUser, Course, UserCourse, Video, ContactUs

admin.site.register(CustomUser)
admin.site.register(Course)
admin.site.register(UserCourse)
admin.site.register(Video)
admin.site.register(ContactUs)
