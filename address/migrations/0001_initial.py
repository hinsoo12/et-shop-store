# Generated by Django 3.2.5 on 2023-06-09 07:47

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
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('building', models.CharField(blank=True, max_length=120, null=True)),
                ('area', models.CharField(blank=True, max_length=100, null=True, verbose_name='Area')),
                ('city', models.CharField(max_length=50, verbose_name='City/Town')),
                ('district', models.CharField(choices=[('Addis Ababa', 'Addis Ababa'), ('Sheger City', 'Sheger City'), ('Adama', 'Adama'), ('Bishoftu', 'Bishoftu'), ('Mojo', 'Mojo'), ('Hawassa', 'Hawassa'), ('Arba-Minch', 'Arba-Minch'), ('Woliata-Soddo', 'Woliata-Soddo'), ('Dire Dewa', 'Dire Dawa'), ('Harar', 'Harar'), ('Jimma', 'Jimma'), ('Bahirdar', 'Bahirdar'), ('Gondar', 'Gondar'), ('Mekele', 'Mekele'), ('Bahirdar', 'Bahirdar')], default='Kathmandu', max_length=100, verbose_name='District')),
                ('province', models.CharField(choices=[('one', 'Province No. 1'), ('two', 'Province No. 2'), ('three', 'Province No. 3'), ('four', 'Province No. 4')], default='three', max_length=100, verbose_name='Province')),
                ('default', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Address',
                'verbose_name_plural': 'Address',
                'ordering': ('-created',),
            },
        ),
    ]