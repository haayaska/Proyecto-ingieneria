# Generated by Django 4.2.4 on 2023-12-05 02:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_userprofile_groups_userprofile_is_active_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='username',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
