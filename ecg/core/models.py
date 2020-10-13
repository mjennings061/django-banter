from django.db import models
from django.contrib.auth.models import User     # import django's model for the user
import uuid     # used for unique ID generation
import os   # used for filename changes
from django.conf import settings
import matlab.engine


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
    format = models.ForeignKey(FileFormat, on_delete=models.CASCADE, related_name='formats',
                               default=FileFormat.objects.values('name')[0])

    def __str__(self):
        return f"{self.user} - {self.name}"


class Script(models.Model):
    """Admin-uploaded algorithms

    identifier          Descriptive ID of the algorithm and owner e.g. 'mat.mj.lowpass_filter'
    description         User description
    language            Programming language used e.g. 'MATLAB'
    supported_input     Supported file inputs. Linked to FileFormat
    output_format       Output format from the algorithm. Linked to FileFormat
    uploaded_script The script file itself

    """
    def script_path(instance, filename):   # dynamic filename changing for the uploaded file when saving
        filename_output = "algorithm/%s" % filename   # filename is username_id.ext e.g mj_45ds.jpeg
        return os.path.join(settings.MEDIA_ROOT, filename_output)  # return filepath for storage

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
                                        default=FileFormat.objects.values('name')[0])
    output_format = models.ForeignKey(FileFormat, on_delete=models.CASCADE, related_name='output_formats',
                                      default=FileFormat.objects.values('name')[0])
    uploaded_script = models.FileField(upload_to=script_path, null=True, max_length=200)  # the file itself

    def __str__(self):
        return self.identifier


class Execution(models.Model):
    """File-Script-Result pair for executing scripts

    identifier          Unique ID of the instance
    data_file           The file to be processed
    script              The executable file to process the file
    result              The result of executing data_file

    """
    def run_file(self):
        if self.script.language == "M":     # if the script is a MATLAB file
            self.eng = matlab.engine.connect_matlab()  # connect to an open MATLAB window open at ecg\media
            self.eng.addpath(   # add the algorithms folder to the MATLAB path
                r'C:\Users\MJ\OneDrive - Ulster University\Documents\PhD\Django\django-banter\ecg\media\algorithm',
                nargout=0)
            # TODO: change this to run the script specified in Execution.script
            file_id = self.eng.LPF_single_row(self.data_input.uploaded_file.path, nargout=1)  # run file through MATLAB
            self.eng.quit()         # stop the MATLAB engine for this instance
            if file_id is not 0:    # if the script processed ok
                result_file = File(     # create an instance of File to store the result file in
                    name=f"result_{int(file_id)}",     # the file name is the same as the MATLAB output
                    user=self.data_input.user,         # user is required to attach the files to
                    format=self.script.output_format,  # format is derived from the script's default format
                    uploaded_file=os.path.join(settings.MEDIA_ROOT, f"results/{int(file_id)}.csv"),
                )
                result_file.save()
                self.data_output = result_file  # save all of result_file to data_output
        # TODO: Add a python run option
        if self.script.language == "P":
            file_id = 0
        return file_id

    identifier = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  # unique ID for the file
    data_input = models.ForeignKey(File, on_delete=models.CASCADE, related_name='data_input', default=None)
    script = models.ForeignKey(Script, on_delete=models.CASCADE, related_name='script', default=None)
    data_output = models.ForeignKey(File, on_delete=models.CASCADE, related_name='data_output', null=True)

    def __str__(self):
        return f"{self.data_output}"
