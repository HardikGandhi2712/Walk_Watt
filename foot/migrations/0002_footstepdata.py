# Generated by Django 4.2.3 on 2024-10-04 04:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foot', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FootstepData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location_name', models.CharField(max_length=100)),
                ('footsteps', models.IntegerField()),
                ('energy_generated', models.FloatField()),
                ('date_recorded', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
