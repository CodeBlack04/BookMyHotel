# Generated by Django 4.2.7 on 2023-11-11 13:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0011_alter_hotel_amenities_alter_rating_amenities_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='amenity',
            options={'ordering': ['created_at']},
        ),
    ]