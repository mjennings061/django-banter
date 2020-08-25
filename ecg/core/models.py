from django.db import models
from django.contrib.auth.models import User     # import django's model for the user
import uuid
import os   # used for filename changes
from django.conf import settings
from django.core.files.storage import FileSystemStorage


# Uploaded file model (connects to UploadedFileForm)
class File(models.Model):
    def content_filename(instance, filename):   # dynamic filename changing for the uploaded file
        ext = filename.split('.')[-1]
        filename = "%s_%s.%s" % (instance.user, instance.id, ext)
        return os.path.join(settings.MEDIA_ROOT, filename)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, default='1')
    uploaded_file = models.FileField(upload_to=content_filename, null=True, max_length=200)

    def __str__(self):
        return self.id
