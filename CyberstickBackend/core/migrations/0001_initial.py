# Generated by Django 4.0.5 on 2022-07-12 21:59

import core.models
import django.contrib.auth.models
import django.contrib.auth.validators
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=255, verbose_name='first name')),
                ('last_name', models.CharField(max_length=255, verbose_name='last name')),
                ('street_address', models.CharField(max_length=255, verbose_name='street address')),
                ('country', models.CharField(max_length=150, verbose_name='country')),
                ('zip_code', models.CharField(max_length=6, verbose_name='zip code')),
                ('city_state', models.CharField(max_length=85, verbose_name='city or state')),
                ('email', models.EmailField(max_length=255, verbose_name='email')),
                ('phone_number', models.CharField(blank=True, max_length=20, validators=[django.core.validators.RegexValidator(regex='^\\+?(234)?\\d{9,15}$')])),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='visit date')),
            ],
            options={
                'verbose_name': 'Customer',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=225, unique=True, verbose_name='product name')),
                ('tags', models.IntegerField(choices=[(1, 'Smart device')], default=1, verbose_name='tags')),
                ('color', models.CharField(choices=[('black', 'Black'), ('red', 'Red'), ('green', 'Green'), ('blue', 'Blue')], default='black', max_length=5)),
                ('price', models.DecimalField(decimal_places=2, default=25000.0, max_digits=10)),
                ('inventory', models.IntegerField(default=1000)),
                ('date', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Product',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='serial number')),
                ('amount', models.IntegerField(default=1)),
                ('color', models.CharField(choices=[('black', 'Black'), ('red', 'Red'), ('green', 'Green'), ('blue', 'Blue')], default='black', max_length=5)),
                ('total_price', models.DecimalField(decimal_places=2, default=25000.0, max_digits=11, verbose_name='price (ngn)')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='order date')),
                ('status', models.IntegerField(choices=[(1, 'not made'), (2, 'made'), (3, 'pending'), (4, 'completed'), (5, 'canceled')], default=1, verbose_name='status')),
                ('customer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.customer')),
                ('item', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='core.product')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('phone_number', models.CharField(blank=True, max_length=20, validators=[django.core.validators.RegexValidator(regex='^\\+?(234)?\\d{9,15}$')])),
                ('address', models.CharField(max_length=255, verbose_name='address')),
                ('image', models.ImageField(upload_to=core.models.user_directory_path)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
