# Generated by Django 4.2.6 on 2023-11-28 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_choicepoll_created_date_datetimepoll_created_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='choicepoll',
            name='ends_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='datetimepoll',
            name='ends_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='rankingpoll',
            name='ends_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='tierlistpoll',
            name='ends_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
