# Generated by Django 4.2 on 2023-04-27 08:27

from django.db import migrations, models
import imagekit.models.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Track',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='', max_length=255)),
                ('description', models.CharField(blank=True, default='', max_length=255, null=True)),
                ('usd_price', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True)),
                ('jpy_price', models.IntegerField(blank=True, default=0, null=True)),
                ('slug', models.SlugField()),
                ('track', models.FileField(blank=True, null=True, upload_to='tracks')),
                ('opus_track', models.FileField(blank=True, null=True, upload_to='opus_tracks')),
                ('sample', models.FileField(blank=True, null=True, upload_to='samples')),
                ('cover_art_v2', imagekit.models.fields.ProcessedImageField(blank=True, max_length=255, null=True, upload_to='cover_art')),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('is_free', models.BooleanField(blank=True, default=False, null=True)),
                ('song_dur', models.CharField(blank=True, default='', max_length=255, null=True)),
                ('downloads', models.IntegerField(blank=True, default=0)),
            ],
            options={
                'db_table': 'tracks',
            },
        ),
    ]
