# Generated by Django 5.0.5 on 2024-05-08 21:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expense', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='expense',
            name='title',
            field=models.TextField(max_length=50, null=True, verbose_name='Titulo del gasto'),
        ),
    ]
