# Generated by Django 3.1.1 on 2020-10-02 21:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainsite', '0006_auto_20201003_0009'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='quantity_required',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
