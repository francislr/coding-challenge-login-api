# Generated by Django 2.1.5 on 2019-02-09 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AttemptEvent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_created', models.DateTimeField(auto_now_add=True)),
                ('username', models.CharField(max_length=150)),
                ('ip_address', models.GenericIPAddressField()),
                ('user_agent', models.CharField(max_length=200)),
                ('result', models.CharField(choices=[('FAIL', 'Failure'), ('SUCC', 'Success'), ('DENY', 'Blocked')], max_length=4)),
            ],
        ),
    ]
