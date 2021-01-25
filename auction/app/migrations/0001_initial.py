# Generated by Django 3.1.5 on 2021-01-22 14:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('auctionsWon', models.TextField()),
                ('auctionsPublished', models.TextField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Auction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30)),
                ('text', models.TextField()),
                ('startPrice', models.FloatField(null=True)),
                ('endPrice', models.FloatField()),
                ('status', models.BooleanField(default=True)),
                ('image', models.ImageField(upload_to='images/')),
                ('startDate', models.DateTimeField(auto_now_add=True)),
                ('endDate', models.DateTimeField()),
                ('hash', models.CharField(default=None, max_length=32, null=True)),
                ('txId', models.CharField(default=None, max_length=66, null=True)),
                ('json', models.TextField(default='')),
                ('advertiser', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='auction_advertiser', to=settings.AUTH_USER_MODEL)),
                ('winner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='auction_winner', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
