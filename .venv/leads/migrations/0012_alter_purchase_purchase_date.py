# Generated by Django 5.0.6 on 2024-07-07 07:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0011_purchase_agent_alter_purchase_amount_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchase',
            name='purchase_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
