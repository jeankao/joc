# Generated by Django 2.2.6 on 2020-07-01 01:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0008_auto_20200601_1659'),
    ]

    operations = [
        migrations.AddField(
            model_name='enroll',
            name='score_annotations',
            field=models.IntegerField(choices=[(100, '你好棒(100分)'), (90, '90分'), (80, '80分'), (70, '70分'), (60, '60分'), (40, '40分'), (20, '20分'), (0, '0分')], default=0, verbose_name='註記成績'),
        ),
        migrations.AlterField(
            model_name='enroll',
            name='score_memo',
            field=models.IntegerField(choices=[(100, '你好棒(100分)'), (90, '90分'), (80, '80分'), (70, '70分'), (60, '60分'), (40, '40分'), (20, '20分'), (0, '0分')], default=0, verbose_name='指定作業心得成績'),
        ),
        migrations.AlterField(
            model_name='enroll',
            name='score_memo2',
            field=models.IntegerField(choices=[(100, '你好棒(100分)'), (90, '90分'), (80, '80分'), (70, '70分'), (60, '60分'), (40, '40分'), (20, '20分'), (0, '0分')], default=0, verbose_name='自訂作業心得成績'),
        ),
    ]
