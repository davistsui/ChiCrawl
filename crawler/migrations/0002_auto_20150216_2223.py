# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crawler', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='address',
            old_name='name',
            new_name='bar',
        ),
        migrations.RenameField(
            model_name='bar',
            old_name='longtitudet',
            new_name='longtitude',
        ),
        migrations.RenameField(
            model_name='bar',
            old_name='bar_name',
            new_name='name',
        ),
    ]
