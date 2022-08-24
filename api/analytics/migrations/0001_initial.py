# Generated by Django 3.2 on 2022-08-20 10:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Analytic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('anonymous_id', models.CharField(max_length=50, null=True)),
                ('title', models.CharField(max_length=50, null=True)),
                ('event', models.CharField(max_length=50, null=True)),
                ('channel', models.CharField(max_length=10, null=True)),
                ('category', models.CharField(max_length=10, null=True)),
                ('resource', models.CharField(max_length=50, null=True)),
                ('url', models.CharField(max_length=50, null=True)),
                ('path', models.CharField(max_length=50, null=True)),
                ('user_id', models.CharField(max_length=50, null=True)),
                ('method', models.CharField(max_length=20, null=True)),
                ('response_time', models.CharField(max_length=10, null=True)),
                ('day', models.CharField(max_length=10, null=True)),
                ('hour', models.CharField(max_length=10, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
    ]