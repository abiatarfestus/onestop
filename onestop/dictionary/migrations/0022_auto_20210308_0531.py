# Generated by Django 3.1.1 on 2021-03-08 03:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dictionary', '0021_auto_20210227_2046'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicaloshindongaidiom',
            name='meaning',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='oshindongaidiom',
            name='meaning',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]