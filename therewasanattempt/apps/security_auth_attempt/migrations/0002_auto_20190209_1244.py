# Generated by Django 2.1.5 on 2019-02-09 17:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('security_auth_attempt', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attemptevent',
            name='user_agent',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
