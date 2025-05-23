# Generated by Django 4.2.20 on 2025-05-10 18:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EmailLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recipient', models.EmailField(max_length=254)),
                ('subject', models.CharField(max_length=255)),
                ('body', models.TextField()),
                ('sent_at', models.DateTimeField(auto_now_add=True)),
                ('app_name', models.CharField(max_length=50)),
                ('record_id', models.CharField(max_length=50)),
            ],
            options={
                'ordering': ['-sent_at'],
            },
        ),
    ]
