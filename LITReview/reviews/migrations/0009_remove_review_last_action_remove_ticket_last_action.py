# Generated by Django 4.2.3 on 2023-08-13 19:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0008_review_last_action_ticket_last_action'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='review',
            name='last_action',
        ),
        migrations.RemoveField(
            model_name='ticket',
            name='last_action',
        ),
    ]