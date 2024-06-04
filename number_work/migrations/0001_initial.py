# Generated by Django 5.0.6 on 2024-05-17 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserNumber',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(max_length=30)),
                ('telecommunication_operator', models.CharField(max_length=100)),
                ('owners_region', models.CharField(max_length=100)),
                ('time_create', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]