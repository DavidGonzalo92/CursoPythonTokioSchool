# Generated by Django 3.1.5 on 2021-01-30 00:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0008_remove_ordenproducto_disponibles'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordenproducto',
            name='cantidad_producto',
            field=models.PositiveIntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='producto',
            name='cantidad',
            field=models.PositiveIntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='producto',
            name='disponibles',
            field=models.PositiveIntegerField(blank=True, default=0, null=True),
        ),
    ]
