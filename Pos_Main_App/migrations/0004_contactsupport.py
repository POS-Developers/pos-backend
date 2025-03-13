# Generated by Django 5.1.6 on 2025-03-04 19:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Pos_Main_App', '0003_remove_bill_model_customer_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactSupport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254)),
                ('phone_number', models.CharField(max_length=15)),
                ('address', models.TextField()),
                ('pin_code', models.CharField(max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
