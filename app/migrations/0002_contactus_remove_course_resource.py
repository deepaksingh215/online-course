# Generated by Django 4.1.9 on 2023-05-20 07:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactUs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('contact_no', models.CharField(max_length=15)),
                ('whatsapp', models.CharField(max_length=15)),
            ],
        ),
        migrations.RemoveField(
            model_name='course',
            name='resource',
        ),
    ]
