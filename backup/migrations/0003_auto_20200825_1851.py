# Generated by Django 3.1 on 2020-08-25 17:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_file_uploaded_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='uploaded_file',
            field=models.FileField(null=True, upload_to='documents/'),
        ),
    ]
