# Generated by Django 3.1.1 on 2020-10-23 16:14

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Algorithm',
            fields=[
                ('identifier', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
            ],
        ),
        migrations.AddField(
            model_name='execution',
            name='algorithm',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='executions', to='core.algorithm'),
        ),
    ]
