# Generated by Django 5.0.4 on 2024-04-27 13:23

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BlogPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(max_length=255, unique=True)),
                ('image', models.CharField(max_length=100)),
                ('author', models.CharField(max_length=100)),
                ('date', models.DateField(default=datetime.date.today)),
                ('title', models.CharField(max_length=255)),
                ('excerpt', models.TextField()),
                ('content', models.TextField()),
            ],
        ),
    ]