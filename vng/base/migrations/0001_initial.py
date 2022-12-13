# Generated by Django 4.1.2 on 2022-12-13 12:50

import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='LicenseDatabaseS3Link',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('license_number', models.CharField(max_length=100, null=True)),
                ('license_data_json', models.FileField(upload_to='license_data/')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('uid', models.CharField(max_length=500, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='TargetImage',
            fields=[
                ('image_id', models.CharField(max_length=500, primary_key=True, serialize=False)),
                ('image', models.FileField(upload_to='media/')),
                ('title', models.CharField(max_length=255, null=True)),
                ('image_name', models.CharField(max_length=255, null=True)),
                ('date', models.DateField(default=django.utils.timezone.now, null=True)),
                ('time', models.TimeField(auto_now_add=True, null=True)),
                ('geom', django.contrib.gis.db.models.fields.PointField(null=True, srid=4326)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.user')),
            ],
        ),
        migrations.CreateModel(
            name='LicensePlate',
            fields=[
                ('license_plate_id', models.CharField(max_length=500, primary_key=True, serialize=False)),
                ('license_number', models.CharField(max_length=100, null=True)),
                ('date', models.DateField(default=django.utils.timezone.now, null=True)),
                ('time', models.TimeField(auto_now_add=True, null=True)),
                ('geom', django.contrib.gis.db.models.fields.PointField(null=True, srid=4326)),
                ('target_image', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.targetimage')),
            ],
        ),
        migrations.CreateModel(
            name='History',
            fields=[
                ('hid', models.CharField(max_length=500, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=200, null=True)),
                ('image_url', models.CharField(max_length=500, null=True)),
                ('date', models.DateField(default=django.utils.timezone.now, null=True)),
                ('time', models.TimeField(auto_now_add=True, null=True)),
                ('isProcessed', models.BooleanField(default=False)),
                ('image', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.targetimage')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.user')),
            ],
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('company_id', models.CharField(max_length=500, primary_key=True, serialize=False)),
                ('place_api_company_name', models.CharField(max_length=255, null=True)),
                ('bovag_matched_name', models.CharField(max_length=255, null=True)),
                ('poitive_reviews', models.IntegerField(null=True)),
                ('negative_reviews', models.IntegerField(null=True)),
                ('rating', models.CharField(max_length=255, null=True)),
                ('duplicate_location', models.CharField(max_length=50, null=True)),
                ('kvk_tradename', models.TextField(null=True)),
                ('irregularities', models.CharField(max_length=50, null=True)),
                ('duplicates_found', models.CharField(max_length=50, null=True)),
                ('Bovag_registered', models.CharField(max_length=50, null=True)),
                ('KVK_found', models.CharField(max_length=50, null=True)),
                ('company_ratings', models.CharField(max_length=50, null=True)),
                ('latitude', models.CharField(max_length=255, null=True)),
                ('longitude', models.CharField(max_length=255, null=True)),
                ('geom', django.contrib.gis.db.models.fields.PointField(null=True, srid=4326)),
                ('image_url', models.CharField(max_length=500, null=True)),
                ('date', models.DateField(default=django.utils.timezone.now, null=True)),
                ('time', models.TimeField(auto_now_add=True, null=True)),
                ('target_image', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.targetimage')),
            ],
            options={
                'verbose_name_plural': 'Companies',
            },
        ),
    ]
