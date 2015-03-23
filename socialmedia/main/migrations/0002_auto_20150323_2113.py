# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Authors',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('host', models.CharField(max_length=32)),
                ('displayname', models.CharField(max_length=32)),
                ('password', models.CharField(max_length=32)),
                ('github', models.CharField(max_length=40)),
                ('approved_flag', models.IntegerField(max_length=8)),
                ('url', models.CharField(max_length=257)),
                ('guid', models.CharField(max_length=32)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('comments', models.CharField(max_length=512)),
                ('pubDate', models.DateField(max_length=32)),
                ('guid', models.CharField(max_length=32)),
                ('author', models.ManyToManyField(to='main.Authors')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Follows',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('authorguid1', models.CharField(max_length=32)),
                ('authorguid2', models.CharField(max_length=32)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.DeleteModel(
            name='Users',
        ),
        migrations.RenameField(
            model_name='posts',
            old_name='extra',
            new_name='categories',
        ),
        migrations.RenameField(
            model_name='posts',
            old_name='post',
            new_name='content_type',
        ),
        migrations.RenameField(
            model_name='posts',
            old_name='date',
            new_name='pubDate',
        ),
        migrations.RemoveField(
            model_name='friends',
            name='followflag',
        ),
        migrations.RemoveField(
            model_name='friends',
            name='username1',
        ),
        migrations.RemoveField(
            model_name='friends',
            name='username2',
        ),
        migrations.RemoveField(
            model_name='posts',
            name='privateFlag',
        ),
        migrations.AddField(
            model_name='friends',
            name='accepted',
            field=models.CharField(default=0, max_length=8),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='friends',
            name='authorguid1',
            field=models.CharField(default=0, max_length=32),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='friends',
            name='authorguid2',
            field=models.CharField(default=0, max_length=32),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='posts',
            name='comments',
            field=models.ManyToManyField(to='main.Comments'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='posts',
            name='content',
            field=models.CharField(default='null', max_length=512),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='posts',
            name='description',
            field=models.CharField(default='null', max_length=256),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='posts',
            name='guid',
            field=models.CharField(default=0, max_length=32),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='posts',
            name='origin',
            field=models.CharField(default=0, max_length=256),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='posts',
            name='source',
            field=models.CharField(default=0, max_length=256),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='posts',
            name='title',
            field=models.CharField(default='null', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='posts',
            name='visibility',
            field=models.CharField(default=0, max_length=16),
            preserve_default=False,
        ),
    ]
