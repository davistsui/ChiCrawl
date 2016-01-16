# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('address_1', models.CharField(max_length=128)),
                ('address_2', models.CharField(max_length=128)),
                ('city', models.CharField(default=b'Chicago', max_length=64)),
                ('state', models.CharField(default=b'Illinois', max_length=30)),
                ('zip_code', models.CharField(default=b'60615', max_length=5)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Bar',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('bar_name', models.CharField(max_length=60)),
                ('lattitue', models.FloatField()),
                ('longtitudet', models.FloatField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='address',
            name='name',
            field=models.ForeignKey(to='crawler.Bar'),
            preserve_default=True,
        ),
    ]
