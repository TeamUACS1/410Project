# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Friends',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('username1', models.CharField(max_length=256)),
                ('username2', models.CharField(max_length=256)),
                ('followflag', models.CharField(max_length=3)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Posts',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('post', models.CharField(max_length=256)),
                ('author', models.CharField(max_length=32)),
                ('date', models.DateField(max_length=32)),
                ('privateFlag', models.IntegerField(max_length=32)),
                ('extra', models.CharField(max_length=32)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('username', models.CharField(max_length=256)),
                ('password', models.CharField(max_length=32)),
                ('githubUsername', models.CharField(max_length=256)),
                ('approved_flag', models.IntegerField(max_length=256)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
