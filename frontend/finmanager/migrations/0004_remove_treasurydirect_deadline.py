# Generated by Django 4.2.13 on 2024-05-16 13:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('finmanager', '0003_alter_treasurydirect_deadline'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='treasurydirect',
            name='deadline',
        ),
    ]