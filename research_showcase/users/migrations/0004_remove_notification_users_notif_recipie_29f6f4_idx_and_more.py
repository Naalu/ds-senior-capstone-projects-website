# Generated by Django 5.1.6 on 2025-04-13 09:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_notification'),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name='notification',
            name='users_notif_recipie_29f6f4_idx',
        ),
        migrations.AddField(
            model_name='notification',
            name='link',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='notification',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
