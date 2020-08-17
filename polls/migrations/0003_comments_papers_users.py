# Generated by Django 3.0.8 on 2020-08-17 01:18

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('polls', '0002_auto_20200816_1818'),
    ]

    operations = [
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('iros2020_name', models.CharField(max_length=100)),
                ('iros2020_email', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Papers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('paper_id', models.PositiveIntegerField(default=0, null=True)),
                ('paper_hitcount', models.PositiveIntegerField(default=0, null=True)),
                ('like_users', models.ManyToManyField(blank=True, related_name='like_papers', to=settings.AUTH_USER_MODEL)),
                ('save_users', models.ManyToManyField(blank=True, related_name='save_papers', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('paper_id', models.PositiveIntegerField(default=0, null=True)),
                ('comment', models.TextField(max_length=1500)),
                ('comment_users', models.ManyToManyField(blank=True, related_name='comment_papers', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
