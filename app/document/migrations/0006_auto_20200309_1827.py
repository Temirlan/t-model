# Generated by Django 3.0.4 on 2020-03-09 12:27

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('document', '0005_document_is_parsed'),
    ]

    operations = [
        migrations.AddField(
            model_name='pdfdocument',
            name='metadata',
            field=django.contrib.postgres.fields.jsonb.JSONField(default=dict),
        ),
        migrations.AddField(
            model_name='pdfdocument',
            name='text',
            field=models.FileField(max_length=500, null=True, upload_to='media/texts/%Y/%m/%d'),
        ),
    ]
