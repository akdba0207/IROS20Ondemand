# Generated by Django 3.0.8 on 2020-08-04 00:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
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
    ]
