# Generated by Django 4.2.7 on 2023-11-11 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0012_alter_amenity_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='hotel',
            name='location_type',
            field=models.CharField(choices=[('UR', 'Urban'), ('AP', 'Airport'), ('RE', 'Resort'), ('BF', 'Beachfront'), ('BO', 'Boutique'), ('BB', 'Bed and Breakfast'), ('EC', 'Eco'), ('HW', 'Highway'), ('SK', 'Ski'), ('CA', 'Casino'), ('CO', 'Conference')], default='UR', max_length=2),
        ),
    ]
