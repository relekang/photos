# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='photo',
            name='slug',
            field=models.CharField(db_index=True, blank=True, unique=True, max_length=160),
            preserve_default=True,
        ),
    ]
