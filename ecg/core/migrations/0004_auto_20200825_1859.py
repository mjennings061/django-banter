# Generated by Django 3.1 on 2020-08-25 17:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20200825_1851'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='name',
            field=models.CharField(default='1', max_length=100),
        ),
    ]
