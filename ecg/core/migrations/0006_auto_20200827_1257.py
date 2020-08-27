# Generated by Django 3.1 on 2020-08-27 11:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20200827_1244'),
    ]

    operations = [
        migrations.AlterField(
            model_name='algorithm',
            name='output_format',
            field=models.ForeignKey(default=({'name': 'CSV File - Single Row'},), on_delete=django.db.models.deletion.CASCADE, related_name='output_formats', to='core.fileformat'),
        ),
        migrations.AlterField(
            model_name='algorithm',
            name='supported_input',
            field=models.ForeignKey(default=({'name': 'CSV File - Single Row'},), on_delete=django.db.models.deletion.CASCADE, related_name='supported_inputs', to='core.fileformat'),
        ),
        migrations.AlterField(
            model_name='file',
            name='format',
            field=models.ForeignKey(default=({'name': 'CSV File - Single Row'},), on_delete=django.db.models.deletion.CASCADE, to='core.fileformat'),
        ),
    ]
