# Generated by Django 4.2.7 on 2023-11-12 12:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0015_hotelroom_room_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='hotelroom',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]