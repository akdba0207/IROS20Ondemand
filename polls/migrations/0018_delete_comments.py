# Generated by Django 3.0.8 on 2020-08-09 19:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0017_comments'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Comments',
        ),
    ]
