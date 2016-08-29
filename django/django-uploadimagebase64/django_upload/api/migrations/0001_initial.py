# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UploadImage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('document', models.TextField()),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('comments', models.TextField(null=True)),
            ],
            options={
                'db_table': 'uploadimage',
            },
        ),
    ]
