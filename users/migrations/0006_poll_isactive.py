# Generated by Django 4.1.1 on 2022-09-28 13:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_userpoll'),
    ]

    operations = [
        migrations.AddField(
            model_name='poll',
            name='isActive',
            field=models.BooleanField(default=True),
        ),
    ]