# Generated by Django 4.2.6 on 2023-10-30 02:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_profile_alter_comment_commenter_alter_friend_friend_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='comment_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='profile',
            name='friend_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='profile',
            name='like_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='profile',
            name='shares_count',
            field=models.IntegerField(default=0),
        ),
    ]
