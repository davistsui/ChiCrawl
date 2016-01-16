# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crawler', '0002_auto_20150216_2223'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bar',
            old_name='lattitue',
            new_name='latitue',
        ),
        migrations.RenameField(
            model_name='bar',
            old_name='longtitude',
            new_name='longitude',
        ),
    ]
