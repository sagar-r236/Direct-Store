# Generated by Django 4.1.4 on 2022-12-21 16:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("MainApp", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="otp",
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
