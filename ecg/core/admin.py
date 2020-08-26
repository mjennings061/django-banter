from django.contrib import admin
from .models import File


# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ['user, id, name, uploaded_file']


admin.site.register(File)
