# Generated by Django 4.1.4 on 2023-01-03 13:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("shop", "0007_rename_shop_name_product_shop_number"),
    ]

    operations = [
        migrations.RenameField(
            model_name="product",
            old_name="shop_number",
            new_name="shop_name",
        ),
    ]