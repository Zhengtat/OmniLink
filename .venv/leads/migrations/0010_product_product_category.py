# Generated by Django 5.0.6 on 2024-07-06 17:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0009_alter_agent_id_alter_category_id_alter_product_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='product_category',
            field=models.CharField(choices=[('Electronic Appliances', 'Electronic Appliances'), ('Skincare', 'Skincare'), ('Kitchen & Dining', 'Kitchen & Dining'), ('Toys', 'Toys'), ('Mobile Accessories', 'Mobile Accessories'), ('Goceries', 'Goceries')], default='Toys', max_length=50),
            preserve_default=False,
        ),
    ]
