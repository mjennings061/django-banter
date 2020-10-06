# Generated by Django 3.1.1 on 2020-10-06 19:02

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_auto_20201006_1704'),
    ]

    operations = [
        migrations.CreateModel(
            name='Execution',
            fields=[
                ('identifier', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('data_input', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='data_input', to='core.file')),
                ('data_output', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='data_output', to='core.file')),
                ('script', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='script', to='core.script')),
            ],
        ),
    ]
