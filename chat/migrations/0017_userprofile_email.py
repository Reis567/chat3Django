# Generated by Django 4.2.5 on 2023-09-24 18:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0016_remove_userprofile_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='email',
            field=models.EmailField(default='email@email.com', max_length=254, null=True),
        ),
    ]