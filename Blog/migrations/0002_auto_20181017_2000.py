# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-10-17 12:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Blog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='About',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.TextField(verbose_name='内容')),
            ],
            options={
                'verbose_name': '关于我',
                'verbose_name_plural': '关于我',
            },
        ),
        migrations.AlterModelOptions(
            name='article',
            options={'ordering': ['-last_modified_time'], 'verbose_name': '博客数据', 'verbose_name_plural': '博客数据'},
        ),
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': '博客分类', 'verbose_name_plural': '博客分类'},
        ),
        migrations.AlterField(
            model_name='article',
            name='status',
            field=models.CharField(choices=[('d', 'Draft'), ('p', 'Published')], max_length=1, verbose_name='文章状态'),
        ),
    ]
