# Generated by Django 5.0.6 on 2024-07-06 13:33

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0007_lead_converted_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=300)),
                ('description', models.TextField()),
                ('unit_price', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.RemoveField(
            model_name='lead',
            name='converted_date',
        ),
        migrations.RemoveField(
            model_name='lead',
            name='date_added',
        ),
        migrations.RemoveField(
            model_name='lead',
            name='phone_number',
        ),
        migrations.AddField(
            model_name='lead',
            name='contact_info',
            field=models.TextField(default='hello'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='agent',
            name='id',
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='category',
            name='id',
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='user',
            name='id',
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='id',
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('payment_method', models.CharField(choices=[('Credit/Debit', 'Credit/Debit'), ('Cash', 'Cash'), ('Grab Paylater', 'Grab Paylater'), ('Bank Transfer', 'Bank Transfer'), ('Reward Points', 'Reward Points'), ('PayPal', 'PayPal')], max_length=100)),
                ('purchase_date', models.DateTimeField()),
                ('quantity', models.PositiveIntegerField()),
                ('lead', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='leads.lead')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='leads.product')),
            ],
        ),
        migrations.CreateModel(
            name='ToDo',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('description', models.TextField()),
                ('due_date', models.DateTimeField()),
                ('assigned_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assigned_todos', to='leads.agent')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_todos', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Reminder',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('remind_at', models.DateTimeField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('todo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='leads.todo')),
            ],
        ),
    ]
