# Generated by Django 2.0.3 on 2019-01-22 06:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='csorders',
            options={'managed': False, 'ordering': ('-initiated_at',)},
        ),
    ]