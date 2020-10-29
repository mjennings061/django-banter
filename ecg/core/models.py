from django.db import models
from django.contrib.auth.models import User     # import django's model for the user
import uuid     # used for unique ID generation
import os   # used for filename changes
from django.conf import settings
import matlab.engine
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver


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


# TODO: create a delete method to remove files
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
        # filename is username_id.ext e.g mj_45ds.m
        filename = "user_data/%s_%s.%s" % (instance.user, instance.identifier, ext)
        return os.path.join(settings.MEDIA_ROOT, filename)  # return filepath for storage

    user = models.ForeignKey(User, on_delete=models.CASCADE)    # link to the user uploading the file
    identifier = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  # unique ID for the file
    name = models.CharField(max_length=100, default=' ')    # user-given name for the file
    uploaded_file = models.FileField(upload_to=content_filename, null=True, max_length=200)     # the file itself
    format = models.ForeignKey(FileFormat, on_delete=models.CASCADE, related_name='formats',
                               default=FileFormat.objects.values('name')[0])

    def __str__(self):
        return f"{self.user}-{self.name}"


class Script(models.Model):
    """Admin-uploaded algorithms

    identifier          Descriptive ID of the algorithm and owner e.g. 'mat.mj.lowpass_filter'
    description         User description
    language            Programming language used e.g. 'MATLAB'
    data_input          Supported file inputs. Linked to FileFormat
    data_output         Output format from the algorithm. Linked to FileFormat
    uploaded_script     The script file itself

    """
    def script_path(instance, filename):
        """ Dynamic filename changing for the uploaded file when saving """
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
    data_input = models.ForeignKey(FileFormat, on_delete=models.CASCADE, related_name='script_inputs',
                                   default=FileFormat.objects.values('name')[0])
    data_output = models.ForeignKey(FileFormat, on_delete=models.CASCADE, related_name='script_outputs',
                                    default=FileFormat.objects.values('name')[0])
    uploaded_script = models.FileField(upload_to=script_path, null=True, max_length=200)  # the file itself

    def __str__(self):
        return self.identifier


class Algorithm(models.Model):
    """Executing an input file from a chain of scripts

    identifier      Unique ID of the instance
    user            The user executing the algorithm
    name            User-defined name for their algorithm
    description     User-defined description
    scripts         The chain of executable files to run

    """
    def save_executions(self, fields):
        """ Get scripts from form data and create instances of Execution """
        scripts = {}
        execution = []
        keys = [key for key in fields if key.startswith('script')]  # get all keys matching 'script'
        for i, key in enumerate(keys):  # for each key of the cleaned_data keys
            scripts[key] = fields[key]  # extract only data with the key 'script'
            if scripts[key] is not None:
                if i == 0:  # the first Execution has its input data pre-defined
                    execution.append(Execution(
                        data_input=fields['data_input'],
                        script=scripts[key],  # linked to Script model
                        algorithm=self,  # linked to Algorithm
                        order=i,  # the order of execution
                    ))
                else:
                    execution.append(Execution(
                        script=scripts[key],
                        algorithm=self,
                        order=i,
                    ))
                execution[i].save()

    def run_algorithm(self):
        """ Run each instance of Execution related to the Algorithm instance """
        executions = Execution.objects.filter(algorithm=self).order_by('order')
        for i, execution in enumerate(executions):
            if i == 0:
                execution.run_file()
            else:
                execution.data_input = executions[i - 1].data_output
                execution.run_file()
            execution.save()

    identifier = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  # unique ID for the instance
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # link to the user creating it
    name = models.CharField(max_length=100)
    description = models.TextField()
    scripts = models.ManyToManyField(Script, through='Execution', related_name="algorithms_related")

    def __str__(self):
        return f"{self.name}"


class Execution(models.Model):
    """File-Script-Result pair for executing scripts

    identifier      Unique ID of the instance
    data_input      The file to be processed
    script          The executable file to process the file
    data_output     The result of executing data_file
    order           The order in which this will run

    """
    def run_file(self):
        """ Run script by passing data_input and producing data_output  """
        if self.script.language == "M":     # if the script is a MATLAB file
            self.eng = matlab.engine.connect_matlab()  # connect to an open MATLAB window open at ecg\media
            data_file_path = self.data_input.uploaded_file.path     # get the datafile path from the model
            script_file_path = self.script.uploaded_script.path     # get the script file path from the model
            file_id = self.eng.handler(script_file_path, data_file_path)    # execute the file by passing thru handler
            self.eng.quit()         # stop the MATLAB engine for this instance
            if file_id is not None or 0:    # if the script processed ok
                result_file = File(     # create an instance of File to store the result file in
                    name=f"result_{int(file_id)}",      # the file name is the same as the MATLAB output
                    user=self.data_input.user,          # user is required to attach the files to
                    format=self.script.data_output,     # format is derived from the script's default format
                    uploaded_file=os.path.join(settings.MEDIA_ROOT, f"results/{int(file_id)}.csv"),
                )
                result_file.save()
                self.data_output = result_file  # save all of result_file to data_output
        # TODO: Add a python run option
        if self.script.language == "P":
            file_id = 0
        return file_id

    identifier = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    data_input = models.ForeignKey(File, on_delete=models.SET_NULL, related_name='execution_inputs', null=True)
    data_output = models.ForeignKey(File, on_delete=models.SET_NULL, related_name='execution_outputs', null=True)
    script = models.ForeignKey(Script, on_delete=models.CASCADE, related_name='execution_scripts', default=None)
    algorithm = models.ForeignKey(Algorithm, on_delete=models.CASCADE, related_name='execution_algorithm', default=None)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.algorithm} - {self.order}-{self.data_output}"


def _delete_file(path):
    """ Deletes file from filesystem. """
    if os.path.isfile(path):
        with open(path) as file:
            file.close()
        os.remove(path)


@receiver(models.signals.post_delete, sender=File)
def delete_file(sender, instance, *args, **kwargs):
    """ Deletes files on post_delete """
    if instance.uploaded_file:
        _delete_file(instance.uploaded_file.path)


@receiver(models.signals.post_delete, sender=Execution)
def delete_execution_files(sender, instance, *args, **kwargs):
    """ Deletes output file related to an Execution instance upon deletion """
    if instance.data_output:
        _delete_file(instance.data_output.uploaded_file.path)
