# Generated by Django 3.2.11 on 2022-01-09 04:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registrations', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentinfo',
            name='roll_no',
            field=models.CharField(blank=True, max_length=100, null=True, unique=True),
        ),
    ]