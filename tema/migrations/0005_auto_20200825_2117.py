# Generated by Django 3.0.8 on 2020-08-26 00:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tema', '0004_auto_20200825_2117'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tema',
            name='slider_1',
            field=models.CharField(choices=[(1, 'Camisetas'), (2, 'Bermudas'), (3, 'Moletons'), (4, 'Destaques')], default=0, max_length=128),
        ),
    ]
