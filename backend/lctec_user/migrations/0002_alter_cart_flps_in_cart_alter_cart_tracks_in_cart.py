# Generated by Django 4.2 on 2023-04-28 03:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracks_app', '0001_initial'),
        ('flps_app', '0001_initial'),
        ('lctec_user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='flps_in_cart',
            field=models.ManyToManyField(blank=True, default=None, null=True, to='flps_app.flp'),
        ),
        migrations.AlterField(
            model_name='cart',
            name='tracks_in_cart',
            field=models.ManyToManyField(blank=True, default=None, null=True, to='tracks_app.track'),
        ),
    ]
