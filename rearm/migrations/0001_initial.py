# Generated by Django 5.2.1 on 2025-05-24 00:10

import django.core.validators
import django.db.models.deletion
import django_ckeditor_5.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AboutSection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('content', django_ckeditor_5.fields.CKEditor5Field(verbose_name='Text')),
                ('image', models.ImageField(help_text='Optimal size: 1200x800px', upload_to='about/')),
                ('meta_title', models.CharField(blank=True, max_length=60)),
                ('meta_description', models.CharField(blank=True, max_length=160)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='CompanyInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('logo', models.ImageField(upload_to='company/')),
                ('address', models.TextField()),
                ('phone_number_1', models.CharField(max_length=20)),
                ('phone_number_2', models.CharField(blank=True, max_length=20, null=True)),
                ('email', models.EmailField(max_length=254)),
            ],
            options={
                'verbose_name_plural': 'Company Info',
            },
        ),
        migrations.CreateModel(
            name='DemoBooking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(max_length=20)),
                ('submitted_at', models.DateTimeField(auto_now_add=True)),
                ('calendly_event_uri', models.URLField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='HeroSection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('page', models.CharField(choices=[('home', 'Home'), ('services', 'Services'), ('products', 'Products'), ('about', 'About Us'), ('contact', 'Contact Us')], max_length=20, unique=True)),
                ('background_image', models.ImageField(upload_to='hero/')),
                ('title', models.CharField(max_length=100)),
                ('subtitle', models.TextField(blank=True)),
                ('primary_cta_text', models.CharField(blank=True, help_text="Main button text (e.g. 'Get Started')", max_length=50)),
                ('primary_cta_link', models.CharField(blank=True, help_text="Examples:<br>- URL name: 'services'<br>- Path: '/services/'<br>- Full URL: 'https://example.com'", max_length=200, validators=[django.core.validators.RegexValidator(message="Enter either: (1) URL name (e.g. 'services'), (2) Path (e.g. '/services/'), or (3) Full URL", regex='^(https?://|/|[\\w-]+$)')])),
                ('secondary_cta_text', models.CharField(blank=True, help_text="Secondary button text (e.g. 'Learn More')", max_length=50)),
                ('secondary_cta_link', models.CharField(blank=True, help_text="Examples:<br>- URL name: 'services'<br>- Path: '/services/'<br>- Full URL: 'https://example.com'", max_length=200, validators=[django.core.validators.RegexValidator(message="Enter either: (1) URL name (e.g. 'services'), (2) Path (e.g. '/services/'), or (3) Full URL", regex='^(https?://|/|[\\w-]+$)')])),
            ],
        ),
        migrations.CreateModel(
            name='Leadership',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('title', models.CharField(max_length=100)),
                ('photo', models.ImageField(upload_to='leadership/')),
                ('home_excerpt', models.TextField(help_text='Short message for homepage', max_length=200)),
                ('full_bio', models.TextField(help_text='Full bio for about page')),
                ('is_ceo', models.BooleanField(default=False)),
                ('display_order', models.PositiveIntegerField(default=0)),
            ],
            options={
                'verbose_name_plural': 'Leadership Team',
                'ordering': ['display_order'],
            },
        ),
        migrations.CreateModel(
            name='Navbar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('logo', models.ImageField(upload_to='navbar/')),
                ('site_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='ProductCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('slug', models.SlugField(blank=True, max_length=100, unique=True)),
            ],
            options={
                'verbose_name_plural': 'Product Categories',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('short_description', models.TextField()),
                ('content', django_ckeditor_5.fields.CKEditor5Field(verbose_name='Text')),
                ('image', models.ImageField(upload_to='services/')),
                ('is_featured', models.BooleanField(default=False)),
                ('slug', models.SlugField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='TeamMember',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('position', models.CharField(max_length=100)),
                ('bio', django_ckeditor_5.fields.CKEditor5Field(verbose_name='Text')),
                ('image', models.ImageField(help_text='Optimal size: 600x600px (1:1 ratio)', upload_to='team/')),
                ('image_alt', models.CharField(blank=True, max_length=100)),
                ('linkedin', models.URLField(blank=True)),
                ('twitter', models.URLField(blank=True)),
                ('facebook', models.URLField(blank=True)),
                ('order', models.PositiveIntegerField(default=0)),
                ('is_active', models.BooleanField(default=True)),
                ('show_on_about', models.BooleanField(default=True, help_text='Toggle to display this member on the About page', verbose_name='Show on About Page')),
            ],
            options={
                'verbose_name_plural': 'Team Members',
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('slug', models.SlugField(unique=True)),
                ('product_type', models.CharField(choices=[('type1', 'Processed Products'), ('type2', 'Raw Products')], max_length=50)),
                ('description', models.TextField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('image', models.ImageField(upload_to='products/')),
                ('image_360', models.ImageField(blank=True, null=True, upload_to='products/360/')),
                ('is_featured', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='rearm.productcategory')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='SocialMedia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('platform', models.CharField(choices=[('facebook', 'Facebook'), ('twitter', 'Twitter'), ('instagram', 'Instagram'), ('linkedin', 'LinkedIn'), ('youtube', 'YouTube')], max_length=20)),
                ('url', models.URLField()),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='social_media', to='rearm.companyinfo')),
            ],
        ),
    ]
