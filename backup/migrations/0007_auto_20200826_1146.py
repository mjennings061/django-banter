# Generated by Django 3.1 on 2020-08-26 10:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_auto_20200825_2118'),
    ]

    operations = [
        migrations.CreateModel(
            name='Algorithm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identifier', models.CharField(max_length=250)),
                ('description', models.TextField()),
                ('language', models.CharField(choices=[('M', 'MATLAB Function'), ('P', 'Python Function')], default='M', max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='FileFormat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('io', models.CharField(choices=[('I', 'Input Only'), ('O', 'Output Only'), ('D', 'Input / Output')], default='D', max_length=1)),
                ('extension', models.CharField(max_length=100)),
                ('mime_type', models.CharField(max_length=100)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='InputType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('input_file_type', models.CharField(choices=[('C', 'CSV File'), ('M', 'MAT File (MATLAB)')], default='C', max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='Handler',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identifier', models.CharField(max_length=250)),
                ('description', models.TextField()),
                ('input_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.fileformat')),
                ('output_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.algorithm')),
            ],
        ),
        migrations.AddField(
            model_name='algorithm',
            name='supported_inputs',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.inputtype'),
        ),
    ]
