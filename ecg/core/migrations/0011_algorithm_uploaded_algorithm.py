# Generated by Django 3.1.1 on 2020-09-03 12:10

import core.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_auto_20200827_1716'),
    ]

    operations = [
        migrations.AddField(
            model_name='algorithm',
            name='uploaded_algorithm',
            field=models.FileField(max_length=200, null=True, upload_to=core.models.Algorithm.algorithm_path),
        ),
    ]