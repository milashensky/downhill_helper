# Generated by Django 3.2.13 on 2022-06-16 00:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('races', '0007_rename_file_race_background_image'),
        ('sensors', '0003_sensorsignal_race'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sensorsignal',
            name='contestant',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='signals', to='races.racecontestantqualification'),
        ),
    ]
