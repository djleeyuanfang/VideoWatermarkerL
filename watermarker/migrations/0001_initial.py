# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TranscodingVideo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('clarity', models.PositiveSmallIntegerField(verbose_name='清晰度')),
                ('width', models.PositiveSmallIntegerField(verbose_name='宽')),
                ('height', models.PositiveSmallIntegerField(verbose_name='高')),
                ('path', models.CharField(verbose_name='文件路径', max_length=150, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='VideoFile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('vid', models.CharField(verbose_name='视频ID', max_length=36, unique=True)),
                ('filename', models.CharField(verbose_name='文件名', max_length=100)),
                ('status', models.CharField(verbose_name='状态', max_length=10, default='WAITING', choices=[('WAITING', '等待转码'), ('CODING', '转码中'), ('COMPLETE', '完成'), ('FAILED', '转码失败')])),
                ('up_date', models.DateTimeField(verbose_name='创建时间', auto_now_add=True)),
            ],
        ),
        migrations.AddField(
            model_name='transcodingvideo',
            name='video_file',
            field=models.ForeignKey(verbose_name='视频文件', on_delete=django.db.models.deletion.DO_NOTHING, to='watermarker.VideoFile'),
        ),
    ]
