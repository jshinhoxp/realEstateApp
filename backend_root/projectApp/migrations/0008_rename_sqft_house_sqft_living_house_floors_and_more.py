# Generated by Django 4.2.5 on 2023-09-08 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projectApp', '0007_house_created'),
    ]

    operations = [
        migrations.RenameField(
            model_name='house',
            old_name='sqft',
            new_name='sqft_living',
        ),
        migrations.AddField(
            model_name='house',
            name='floors',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='house',
            name='sqft_lot',
            field=models.IntegerField(default=0),
        ),
    ]