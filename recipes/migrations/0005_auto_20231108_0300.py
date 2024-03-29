# Generated by Django 3.2.21 on 2023-11-08 03:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0004_auto_20231017_2250'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='saves',
            options={'ordering': ['-saved_on']},
        ),
        migrations.AlterField(
            model_name='recipe',
            name='description',
            field=models.TextField(blank=True, help_text='Optional, max length 300 characters.', max_length=300),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='title',
            field=models.CharField(help_text='Required, max length 50 characters.', max_length=50),
        ),
    ]
