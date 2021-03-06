# Generated by Django 2.1.2 on 2020-04-04 12:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DayCounter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.CharField(max_length=8)),
                ('hit', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Domain',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='', max_length=200, verbose_name='領域名稱')),
            ],
        ),
        migrations.CreateModel(
            name='LessonCounter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10)),
                ('hit', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Level',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='', max_length=200, verbose_name='年級')),
            ],
        ),
        migrations.CreateModel(
            name='LogCounter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('counter_id', models.IntegerField(default=0)),
                ('counter_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('counter_ip', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author_id', models.IntegerField(default=0)),
                ('reader_id', models.IntegerField(default=0)),
                ('type', models.IntegerField(default=0)),
                ('classroom_id', models.IntegerField(default=0)),
                ('title', models.CharField(max_length=250)),
                ('content', models.TextField(default='')),
                ('url', models.CharField(max_length=250)),
                ('time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='MessageContent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message_id', models.IntegerField(default=0)),
                ('user_id', models.IntegerField(default=0)),
                ('title', models.CharField(blank=True, max_length=250, null=True)),
                ('filename', models.CharField(blank=True, max_length=250, null=True)),
                ('publication_date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='MessageFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message_id', models.IntegerField(default=0)),
                ('filename', models.TextField()),
                ('before_name', models.TextField()),
                ('upload_date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='MessagePoll',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message_type', models.IntegerField(default=0)),
                ('message_id', models.IntegerField(default=0)),
                ('reader_id', models.IntegerField(default=0)),
                ('classroom_id', models.IntegerField(default=0)),
                ('read', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='PointHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField(default=0)),
                ('kind', models.IntegerField(default=0)),
                ('message', models.CharField(max_length=100)),
                ('url', models.CharField(max_length=100)),
                ('publish', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('work', models.IntegerField(default=0)),
                ('assistant', models.IntegerField(default=0)),
                ('creative', models.IntegerField(default=0)),
                ('forum', models.IntegerField(default=0)),
                ('like', models.FloatField(default=0.0)),
                ('reply', models.FloatField(default=0.0)),
                ('avatar', models.IntegerField(default=0)),
                ('home_count', models.IntegerField(default=0)),
                ('visitor_count', models.IntegerField(default=0)),
                ('open_time', models.DateTimeField(auto_now_add=True)),
                ('classroom', models.TextField()),
                ('lock1', models.IntegerField(default=0)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Visitor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.IntegerField(default=0)),
                ('count', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='VisitorLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('visitor_id', models.IntegerField(default=0)),
                ('user_id', models.IntegerField(default=0)),
                ('time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
