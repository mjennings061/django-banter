from django.contrib import admin
from .models import File, FileFormat, Subprocess    # Algorithm, Handler


# Register your models here.
@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    pass


@admin.register(FileFormat)
class FileFormatAdmin(admin.ModelAdmin):
    pass


@admin.register(Subprocess)
class SubprocessAdmin(admin.ModelAdmin):
    pass

# @admin.register(Algorithm)
# class AlgorithmAdmin(admin.ModelAdmin):
#     pass


# @admin.register(Handler)
# class HandlerAdmin(admin.ModelAdmin):
#     pass
