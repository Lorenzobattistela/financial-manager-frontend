# Generated by Django 4.2.13 on 2024-05-16 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finmanager', '0006_alter_bitcoinaddress_balance_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fii',
            name='updated_value',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20),
        ),
    ]
