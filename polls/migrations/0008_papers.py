# Generated by Django 3.0.8 on 2020-08-04 06:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0007_delete_papers'),
    ]

    operations = [
        migrations.CreateModel(
            name='Papers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('paper_id', models.PositiveIntegerField(default=0, null=True)),
                ('like_users', models.ManyToManyField(blank=True, related_name='like_papers', to='polls.Users')),
            ],
        ),
    ]