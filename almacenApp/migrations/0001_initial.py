# Generated by Django 5.0.3 on 2024-05-27 19:36

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Marca',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Proveedor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('direccion', models.CharField(blank=True, max_length=255, null=True)),
                ('telefono', models.CharField(blank=True, max_length=20, null=True)),
                ('logo', models.ImageField(blank=True, null=True, upload_to='proveedor/')),
            ],
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(blank=True, max_length=100, null=True)),
                ('descripcion', models.TextField()),
                ('muestra', models.ImageField(blank=True, null=True, upload_to='productos/')),
                ('precio', models.DecimalField(decimal_places=2, default=0, max_digits=8)),
                ('estado', models.CharField(choices=[('disponible', 'DISPONIBLE'), ('pedido', 'SIN STOCK')], default='disponible', max_length=20)),
                ('cantidad', models.IntegerField(blank=True, default=0, null=True)),
                ('fecha_entrada', models.DateTimeField(auto_now_add=True)),
                ('categoria', models.ManyToManyField(to='almacenApp.categoria')),
                ('marca', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='almacenApp.marca')),
            ],
        ),
        migrations.CreateModel(
            name='Pedido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad_pedida', models.IntegerField(default=0)),
                ('fecha_pedida', models.DateTimeField(auto_now_add=True)),
                ('estado', models.CharField(choices=[('pedido', 'PEDIDO'), ('finalizado', 'FINALIZADO')], default='pedido', max_length=20)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='almacenApp.producto')),
                ('proveedor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='almacenApp.proveedor')),
            ],
        ),
    ]
