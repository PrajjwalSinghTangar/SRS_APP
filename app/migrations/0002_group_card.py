# Generated by Django 4.1 on 2022-12-03 09:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('group', models.CharField(max_length=64)),
                ('description', models.CharField(max_length=264)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('front', models.CharField(max_length=64)),
                ('back', models.CharField(max_length=128)),
                ('revision', models.DateField()),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.group')),
            ],
        ),
    ]
