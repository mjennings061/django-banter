# Generated by Django 3.1.1 on 2020-10-29 10:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_auto_20201028_2031'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='algorithm',
            options={'ordering': ['execution_algorithm__order']},
        ),
    ]