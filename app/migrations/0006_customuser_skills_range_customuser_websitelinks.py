# Generated by Django 5.0.3 on 2024-04-01 07:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_appliedfor_applied_alter_appliedfor_post'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='skills_range',
            field=models.CharField(blank=True, max_length=256),
        ),
        migrations.AddField(
            model_name='customuser',
            name='websitelinks',
            field=models.CharField(blank=True, max_length=256),
        ),
    ]
