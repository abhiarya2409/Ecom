# Generated by Django 4.2.7 on 2023-12-15 10:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Amazon', '0002_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_image', models.ImageField(upload_to='upload/product/')),
                ('product_name', models.CharField(default='', max_length=100, null=True)),
                ('product_price', models.BigIntegerField(default=1)),
                ('product_description', models.TextField(blank=True, max_length=200, null=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Amazon.category')),
            ],
        ),
    ]
