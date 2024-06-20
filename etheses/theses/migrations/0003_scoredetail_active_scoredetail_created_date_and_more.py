# Generated by Django 5.0.4 on 2024-06-14 04:06

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('theses', '0002_remove_user_gender_remove_user_phone_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='scoredetail',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='scoredetail',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2024, 5, 24, 0, 0)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='scoredetail',
            name='updated_date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
