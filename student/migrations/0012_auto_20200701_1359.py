# Generated by Django 2.0.7 on 2020-07-01 05:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0011_merge_20200701_1355'),
    ]

    operations = [
        migrations.AlterField(
            model_name='work',
            name='comment',
            field=models.TextField(blank=True, default='', null=True, verbose_name='評語回饋'),
        ),
        migrations.AlterField(
            model_name='work',
            name='score',
            field=models.IntegerField(choices=[(-2, ''), (100, '100分'), (90, '90分'), (80, '80分'), (70, '70分'), (60, '60分'), (-1, '重交')], default=-2, verbose_name='成績'),
        ),
    ]