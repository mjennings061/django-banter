from django.contrib import admin
from .models import File, FileFormat, Script, Execution, Algorithm


# Register your models here.
@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    pass


@admin.register(FileFormat)
class FileFormatAdmin(admin.ModelAdmin):
    pass


@admin.register(Script)
class SubprocessAdmin(admin.ModelAdmin):
    pass


@admin.register(Execution)
class ExecutionAdmin(admin.ModelAdmin):
    pass


@admin.register(Algorithm)
class AlgorithmAdmin(admin.ModelAdmin):
    pass
