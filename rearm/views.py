

# Create your views here.

from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from .models import Service
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os
from datetime import datetime
from .forms import DemoBookingForm
from django.conf import settings
import uuid
from django.views.decorators.http import require_GET
from .models import AboutSection, TeamMember, Navbar
from .models import Product
from blog.models import Post
from cloudinary.uploader import upload as cloudinary_upload
from cloudinary.exceptions import Error as CloudinaryError

# def home(request):
#     # Navbar data is already available via context processor
#     return render(request, "rearm/home.html")


def home(request):
    ceo_message = Leadership.objects.filter(is_ceo=True).first() # ceo
    about_content = AboutSection.objects.filter(is_active=True).first()
    featured_services = Service.objects.filter(is_featured=True)[:3]  # Just get 3 featured services
    featured_products = Product.objects.filter(is_featured=True)[:3]  # Get 3 featured products
    blog_posts = Post.objects.filter(is_published=True).order_by('-created_at')[:4]  # Get latest 4 posts
    context = {
        'ceo': ceo_message,
        'blog_posts': blog_posts,
        'about_content': about_content,
        'page_name': 'home',
        'featured_services': featured_services,
        'featured_products': featured_products,
    }
    return render(request, "rearm/home.html", context)

# ----------------------------------------------------



# services page views

def services(request):
    context = {
        'page_name': 'services',  # This matches your HeroSection PAGE_CHOICES
    }
    return render(request, "rearm/services.html", context)





def services(request):
    services = Service.objects.filter(is_featured=True)
    return render(request, 'rearm/services.html', {'services': services})

def service_detail(request, slug):
    service = get_object_or_404(Service, slug=slug)
    return render(request, 'rearm/service_detail.html', {'service': service})



# uploading images to cloudinary

@csrf_exempt
def upload_media(request):
    if request.method == 'POST' and request.FILES:
        try:
            file = request.FILES['file']

            # Upload to Cloudinary under 'media/' folder
            result = cloudinary_upload(file, folder='media/')

            # Return the Cloudinary URL
            return JsonResponse({
                'location': result['secure_url']
            })

        except CloudinaryError as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid upload'}, status=400)




# demon bookings


def book_demo_page(request):
    if request.method == 'POST':
        form = DemoBookingForm(request.POST)
        if form.is_valid():
            booking = form.save()
            
            # Generate unique Calendly link (replace with your actual Calendly URL)
            calendly_url = f"https://meet.brevo.com/rearm-resouces/30-minute-meeting"
            
            
            # Save the Calendly link to the booking
            booking.calendly_event_uri = calendly_url
            booking.save()
            
            return redirect(calendly_url)
    else:
        form = DemoBookingForm()
    
    return render(request, 'book_demo_page.html', {'form': form})



# about us section
from .models import Leadership
@require_GET
def about(request):
    try:
        about_content = AboutSection.objects.filter(is_active=True).latest('id')
        leadership = Leadership.objects.all().order_by('display_order')
    except AboutSection.DoesNotExist:
        about_content = None
    
    team_members = TeamMember.objects.filter(
        is_active=True,
        show_on_about=True
        ).order_by('order')
    
    context = {
        'leadership': leadership,
        'about_content': about_content,
        'team_members': team_members,
        'page_name': 'about',
        'meta_title': getattr(about_content, 'meta_title', 'About Us | Your Company'),
        'meta_description': getattr(about_content, 'meta_description', 'Learn about our company and team'),
        'canonical_url': request.build_absolute_uri(request.path)
    }
    return render(request, 'rearm/about.html', context)







# product section

from django.shortcuts import render, get_object_or_404
from .models import Product, ProductCategory

def product_list(request):
    # Get all active products organized by type
    agricultural = Product.objects.filter(
        product_type='type1', 
        is_active=True
    ).select_related('category')
    
    equipment = Product.objects.filter(
        product_type='type2', 
        is_active=True
    ).select_related('category')
    
    context = {
        'agricultural_products': agricultural,
        'equipment_products': equipment,
    }
    return render(request, 'rearm/products/list.html', context)

# product details page
def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    related_products = Product.objects.filter(
        category=product.category,
        is_active=True
    ).exclude(id=product.id)[:4]  # Get 4 related products
    
    context = {
        'product': product,
        'related_products': related_products,
        }
    return render(request, 'rearm/products/detail.html', context)