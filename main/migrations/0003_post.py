# Generated by Django 5.0.1 on 2024-01-26 21:21

import datetime
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_alter_profile_pro_photo'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('user', models.CharField(max_length=100)),
                ('content', models.ImageField(upload_to='postsimg')),
                ('captions', models.TextField(max_length=120)),
                ('created_at', models.DateTimeField(default=datetime.datetime.now)),
                ('no_likes', models.IntegerField(default=0)),
            ],
        ),
    ]