# Generated by Django 4.2.9 on 2024-01-27 07:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qna_api', '0002_question'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to='user_avatars/'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='is_staff',
            field=models.BooleanField(default=False),
        ),
    ]