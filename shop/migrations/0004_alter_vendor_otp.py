# Generated by Django 4.1.4 on 2023-01-01 13:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("shop", "0003_alter_vendor_otp"),
    ]

    operations = [
        migrations.AlterField(
            model_name="vendor",
            name="otp",
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
    ]