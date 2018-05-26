# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2018-04-27 22:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0005_teacher_age'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='tag',
            field=models.CharField(choices=[('1', '金牌讲师'), ('2', '银牌讲师'), ('3', '铜牌讲师')], default='1', max_length=20, verbose_name='讲师级别'),
        ),
    ]
