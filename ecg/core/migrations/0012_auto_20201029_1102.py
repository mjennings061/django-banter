# Generated by Django 3.1.1 on 2020-10-29 11:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_auto_20201029_1033'),
    ]

    operations = [
        migrations.AlterField(
            model_name='algorithm',
            name='scripts',
            field=models.ManyToManyField(related_name='algorithms_related', related_query_name="{'class': 'algorithm', 'app_label': 'core'}lgorithms", through='core.Execution', to='core.Script'),
        ),
    ]
