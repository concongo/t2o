# Generated by Django 3.2.9 on 2021-12-01 10:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bc_orders', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='OrderBook',
            new_name='Order',
        ),
    ]
