# Generated by Django 3.1.7 on 2021-03-03 14:50

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('admin', '0003_logentry_add_action_flag_choices'),
        ('models', '0002_auto_20210303_1720'),
    ]

    operations = [
        migrations.AddField(
            model_name='anekdot',
            name='rated_by',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='AnekUser',
        ),
    ]