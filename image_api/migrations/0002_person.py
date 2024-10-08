# Generated by Django 5.1 on 2024-08-24 06:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('image_api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='uploads/')),
                ('name', models.CharField(max_length=100)),
                ('father_name', models.CharField(max_length=100)),
                ('date_of_birth', models.DateField()),
            ],
            options={
                'unique_together': {('name', 'father_name', 'date_of_birth')},
            },
        ),
    ]
