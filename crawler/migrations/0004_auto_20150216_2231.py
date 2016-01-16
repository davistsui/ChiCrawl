# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crawler', '0003_auto_20150216_2229'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bar',
            old_name='latitue',
            new_name='latitude',
        ),
    ]
