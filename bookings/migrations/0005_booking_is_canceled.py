# Generated by Django 4.1.5 on 2023-02-10 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("bookings", "0004_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="booking",
            name="is_canceled",
            field=models.BooleanField(default=False),
        ),
    ]