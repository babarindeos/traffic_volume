# Generated by Django 4.2.2 on 2023-07-08 06:57

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_cluster'),
    ]

    operations = [
        migrations.CreateModel(
            name='Node',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('battery', models.IntegerField()),
                ('fault', models.BooleanField()),
                ('headship', models.BooleanField()),
                ('date', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('cluster', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cluster', to='myapp.cluster')),
            ],
        ),
    ]