# Generated by Django 4.0.3 on 2022-04-04 15:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Strategify', '0009_orders'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orders',
            old_name='quantity',
            new_name='message',
        ),
    ]
