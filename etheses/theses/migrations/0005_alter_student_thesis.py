# Generated by Django 5.0.4 on 2024-06-15 07:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('theses', '0004_thesisscore_active_thesisscore_created_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='thesis',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='theses.thesis'),
        ),
    ]
