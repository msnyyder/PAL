# Generated by Django 4.1.7 on 2023-03-30 19:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courseRegistration', '0002_userextended'),
    ]

    operations = [
        migrations.AddField(
            model_name='userextended',
            name='major',
            field=models.CharField(choices=[('math', 'MATH'), ('cs', 'CS')], default='CS', max_length=5),
        ),
    ]
