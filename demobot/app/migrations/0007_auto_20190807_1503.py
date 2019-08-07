# Generated by Django 2.1.7 on 2019-08-07 15:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_auto_20190807_1457'),
    ]

    operations = [
        migrations.AlterField(
            model_name='data',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='data',
            name='user',
            field=models.ForeignKey(db_column='user', on_delete=django.db.models.deletion.DO_NOTHING, to='app.User'),
        ),
        migrations.AlterUniqueTogether(
            name='data',
            unique_together={('user', 'clz')},
        ),
    ]
