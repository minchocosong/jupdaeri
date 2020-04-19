# Generated by Django 3.0.5 on 2020-04-19 11:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restapi', '0002_auto_20200419_1154'),
    ]

    operations = [
        migrations.RenameField(
            model_name='balance',
            old_name='conclusion_count',
            new_name='balance_amount',
        ),
        migrations.RemoveField(
            model_name='balance',
            name='evaluation_amount',
        ),
        migrations.RemoveField(
            model_name='balance',
            name='revenue_rate',
        ),
        migrations.AddField(
            model_name='balance',
            name='cash_credit',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='balance',
            name='conclusion_price',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='balance',
            name='current_price',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='balance',
            name='evaluation_price',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='balance',
            name='loan_date',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='balance',
            name='evaluation_plus_minus',
            field=models.FloatField(null=True),
        ),
    ]
