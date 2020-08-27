from django.db import models
from django.contrib.auth.models import User     # import django's model for the user
import uuid     # used for unique ID generation
import os   # used for filename changes
from django.conf import settings


class FileFormat(models.Model):
    """Specifies file types used for data

    name        Human readable name (e.g. CSV)
    io          Whether the file type is used for input or output or both
    extension   Normally used file extensions (e.g. .csv)
    mime_type   Allowable mimetypes (e.g. text/csv)
    description Detailed description if needed

    """

    INPUT = "I"
    OUTPUT = "O"
    DUPLEX = "D"

    IO_CHOICES = (
        (INPUT, "Input Only"),
        (OUTPUT, "Output Only"),
        (DUPLEX, "Input / Output"),
    )

    name = models.CharField(max_length=100)
    io = models.CharField(max_length=1, choices=IO_CHOICES, default=DUPLEX)
    extension = models.CharField(max_length=100)
    mime_type = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name


# Uploaded file model (connects to UploadedFileForm)
class File(models.Model):
    """Uploaded file model

    user            The user uploading the file
    id              Unique ID given to each instance
    name            User-given name for their file
    uploaded_file   The file itself
    format          The uploaded file format - related to FileFormat

    """
    def content_filename(instance, filename):   # dynamic filename changing for the uploaded file when saving
        ext = filename.split('.')[-1]   # get file extension
        filename = "%s_%s.%s" % (instance.user, instance.id, ext)   # filename is username_id.ext e.g mj_45ds.jpeg
        return os.path.join(settings.MEDIA_ROOT, filename)  # return filepath for storage

    user = models.ForeignKey(User, on_delete=models.CASCADE)    # link to the user uploading the file
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  # unique ID for the file
    name = models.CharField(max_length=100, default=' ')    # user-given name for the file
    uploaded_file = models.FileField(upload_to=content_filename, null=True, max_length=200)     # the file itself
    format = models.ForeignKey(FileFormat, on_delete=models.CASCADE, default=FileFormat.objects.values('name'))

    def __str__(self):
        return f"{self.user}_{self.id}"


class Algorithm(models.Model):
    """Admin-uploaded algorithms

    identifier          Descriptive ID of the algorithm and owner e.g. 'mat.mj.lowpass_filter'
    description         User description
    language            Programming language used e.g. 'MATLAB'
    supported_input     Supported file inputs. Linked to FileFormat
    output_format       Output format from the algorithm. Linked to FileFormat

    """
    MATLAB = "M"
    PYTHON = "P"

    LANGUAGE_CHOICES = (
        (MATLAB, "MATLAB Function"),
        (PYTHON, "Python Function"),
    )

    identifier = models.CharField(max_length=250)
    description = models.TextField()
    language = models.CharField(max_length=1, choices=LANGUAGE_CHOICES, default=MATLAB)
    supported_input = models.ForeignKey(FileFormat, on_delete=models.CASCADE, related_name='supported_inputs',
                                        default=FileFormat.objects.values('name'))
    output_format = models.ForeignKey(FileFormat, on_delete=models.CASCADE, related_name='output_formats',
                                      default=FileFormat.objects.values('name'))
    # possible FileField with the algorithm? Or a path to the file?

    def __str__(self):
        return self.identifier


# TODO design the handler to pass files to fitting functions
# class Handler(models.Model):
#     """Handles the output of one process to the input of another
#
#     identifier      A unique identifier for the handler, also the name of the executable plugin
#     description     Detailed explanation of the handler
#     input_type      Input file type for the chosen algorithm
#
#     """
#
#     identifier = models.CharField(max_length=250)
#     description = models.TextField()
#     input_type = models.ForeignKey(FileFormat, on_delete=models.CASCADE, related_name='output_formats',
#                                    default=FileFormat.objects.values('name'))
#     output_type


# write (box) model for algorithm
# write (arrow) model for single-format handler
# file format model - I/o choice, MIME type, description (opt.)

# allow user to see all files belonging to them
# single file running through single algorithm (for now)
