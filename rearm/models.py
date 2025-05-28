# Create your models here.
from django.db import models
from django.utils.safestring import mark_safe
from django.core.validators import URLValidator
from django.core.validators import RegexValidator
from django.urls import reverse
from django_ckeditor_5.fields import CKEditor5Field 

from django.utils.text import slugify

class Navbar(models.Model):
    logo = models.ImageField(upload_to='navbar/')  # Stores in `media/navbar/`
    site_name = models.CharField(max_length=100)

    def logo_preview(self):
        if self.logo:
            return mark_safe(f'<img src="{self.logo.url}" width="50" />')
        return "No Logo"
    logo_preview.short_description = 'Preview'

    def __str__(self):
        return self.site_name
    

# hero section model
class HeroSection(models.Model):
    PAGE_CHOICES = [
        ('home', 'Home'),
        ('services', 'Services'),
        ('products', 'Products'),
        ('about', 'About Us'),
        ('contact', 'Contact Us'),
    ]
    
    # Core fields
    page = models.CharField(max_length=20, choices=PAGE_CHOICES, unique=True)
    background_image = models.ImageField(upload_to='hero/')
    title = models.CharField(max_length=100)
    subtitle = models.TextField(blank=True)
    
    # CTA Fields (Primary + Secondary)
    primary_cta_text = models.CharField(
        max_length=50,
        blank=True,
        help_text="Main button text (e.g. 'Get Started')"
    )

    primary_cta_link = models.CharField(
        max_length=200,
        blank=True,
        validators=[
            RegexValidator(
                regex=r'^(https?://|/|[\w-]+$)',
                message="Enter either: (1) URL name (e.g. 'services'), (2) Path (e.g. '/services/'), or (3) Full URL"
            )
        ],
        help_text="Examples:<br>"
                 "- URL name: 'services'<br>"
                 "- Path: '/services/'<br>"
                 "- Full URL: 'https://example.com'"
    )

    secondary_cta_text = models.CharField(
        max_length=50,
        blank=True,
        help_text="Secondary button text (e.g. 'Learn More')"
    )
    secondary_cta_link = models.CharField(
        max_length=200,
        blank=True,
        validators=[
            RegexValidator(
                regex=r'^(https?://|/|[\w-]+$)',
                message="Enter either: (1) URL name (e.g. 'services'), (2) Path (e.g. '/services/'), or (3) Full URL"
            )
        ],
        help_text="Examples:<br>"
                 "- URL name: 'services'<br>"
                 "- Path: '/services/'<br>"
                 "- Full URL: 'https://example.com'"
    )

    def __str__(self):
        return f"Hero for {self.get_page_display()}"
    

# services section model

class Service(models.Model):
    title = models.CharField(max_length=200)
    short_description = models.TextField()
    content = CKEditor5Field('Text', config_name='extends') # For rich content
    image = models.ImageField(upload_to='services/')
    is_featured = models.BooleanField(default=False)
    slug = models.SlugField(unique=True)
    
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('service_detail', kwargs={'slug': self.slug})



# CTA
class DemoBooking(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    submitted_at = models.DateTimeField(auto_now_add=True)
    calendly_event_uri = models.URLField(blank=True, null=True)  # To store Calendly link
    
    def __str__(self):
        return f"{self.name} - {self.submitted_at.strftime('%Y-%m-%d')}"
    



# aboutsection model
class AboutSection(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    content = CKEditor5Field('Text', config_name='extends')
    main_image = models.ImageField(
        upload_to='about/', 
        help_text="Main image (1200x800px)",
        null=True,
        blank=True)
    secondary_image = models.ImageField(
        upload_to='about/', 
        help_text="Secondary image (600x400px)",
        null=True,
        blank=True)
    meta_title = models.CharField(max_length=60, blank=True)
    meta_description = models.CharField(max_length=160, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title
    

# team member section
class TeamMember(models.Model):
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    bio = CKEditor5Field('Text', config_name='extends') #use the ckeditor here for the bio
    image = models.ImageField(upload_to='team/', help_text="Optimal size: 600x600px (1:1 ratio)")
    image_alt = models.CharField(max_length=100, blank=True)
    linkedin = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    facebook = models.URLField(blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    show_on_about = models.BooleanField(
        default=True,
        verbose_name="Show on About Page",
        help_text="Toggle to display this member on the About page"
    )

    class Meta:
        ordering = ['order']
        verbose_name_plural = "Team Members"

    def __str__(self):
        return f"{self.name} - {self.position}"
    


# footer model

class CompanyInfo(models.Model):
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='company/')
    address = models.TextField()
    phone_number_1 = models.CharField(max_length=20)
    phone_number_2 = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField()
    
    class Meta:
        verbose_name_plural = "Company Info"
    
    def __str__(self):
        return self.name

class SocialMedia(models.Model):
    PLATFORMS = [
        ('facebook', 'Facebook'),
        ('twitter', 'Twitter'),
        ('instagram', 'Instagram'),
        ('linkedin', 'LinkedIn'),
        ('youtube', 'YouTube'),
    ]
    
    company = models.ForeignKey(CompanyInfo, on_delete=models.CASCADE, related_name='social_media')
    platform = models.CharField(max_length=20, choices=PLATFORMS)
    url = models.URLField()
    
    def icon_class(self):
        return f"fab fa-{self.platform}"
    
    def __str__(self):
        return f"{self.company.name} - {self.get_platform_display()}"
    



from django.urls import reverse
from django.utils.text import slugify

class ProductCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    
    class Meta:
        verbose_name_plural = "Product Categories"
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Product(models.Model):
    PRODUCT_TYPES = (
        ('type1', 'Processed Products'),
        ('type2', 'Raw Products'),
    )

    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(ProductCategory, on_delete=models.PROTECT)
    product_type = models.CharField(max_length=50, choices=PRODUCT_TYPES)
    description = models.TextField()
    # uncomment should you need it in future
    # price = models.DecimalField(max_digits=10, decimal_places=2)

    image = models.ImageField(upload_to='products/')              # Main thumbnail image
    image_360 = models.ImageField(upload_to='products/360/', null=True, blank=True)  # 360° equirectangular image

    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'slug': self.slug})
    



# ceo model


class Leadership(models.Model):
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='leadership/')
    home_excerpt = models.TextField(max_length=200, help_text="Short message for homepage")
    full_bio = models.TextField(help_text="Full bio for about page")
    is_ceo = models.BooleanField(default=False)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['display_order']
        verbose_name_plural = "Leadership Team"

    def __str__(self):
        return f"{self.name} ({'CEO' if self.is_ceo else self.title})"
    





















