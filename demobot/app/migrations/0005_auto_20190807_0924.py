# Generated by Django 2.1.7 on 2019-08-07 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_auto_20190807_0919'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='group',
            name='created_date',
        ),
        migrations.AddField(
            model_name='group',
            name='created_at',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='group',
            name='state',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
