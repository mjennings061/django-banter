# Generated by Django 3.1 on 2020-08-26 13:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='format',
            field=models.ForeignKey(default=({'name': 'CSV File - Single Row'},), on_delete=django.db.models.deletion.CASCADE, to='core.fileformat'),
        ),
    ]