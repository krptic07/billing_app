# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2019-01-15 09:25
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('billapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bill',
            name='current_date',
            field=models.DateField(default=datetime.date.today, verbose_name='Date'),
        ),
    ]