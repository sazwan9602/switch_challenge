# Generated by Django 2.2.10 on 2020-02-19 09:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('switchapp', '0002_switch_switch_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='switch',
            name='switch_status',
            field=models.IntegerField(),
        ),
    ]
