from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET
from django.conf import settings
from .models import (
    Service, 
    AboutSection, 
    TeamMember, 
    Leadership,
    Product,
    ProductCategory
)
from .forms import DemoBookingForm
from blog.models import Post
from cloudinary.uploader import upload
from cloudinary.exceptions import Error as CloudinaryError

def home(request):
    ceo_message = Leadership.objects.filter(is_ceo=True).first()
    about_content = AboutSection.objects.filter(is_active=True).first()
    context = {
        'ceo': ceo_message,
        'blog_posts': Post.objects.filter(is_published=True).order_by('-created_at')[:4],
        'about_content': about_content,
        'page_name': 'home',
        'featured_services': Service.objects.filter(is_featured=True)[:3],
        'featured_products': Product.objects.filter(is_featured=True)[:3],
    }
    return render(request, "rearm/home.html", context)

def services(request):
    # Combined the two service views you had
    services = Service.objects.filter(is_featured=True)
    context = {
        'services': services,
        'page_name': 'services',
    }
    return render(request, "rearm/services.html", context)

def service_detail(request, slug):
    service = get_object_or_404(Service, slug=slug)
    return render(request, 'rearm/service_detail.html', {'service': service})

def book_demo_page(request):
    if request.method == 'POST':
        form = DemoBookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.calendly_event_uri = "https://meet.brevo.com/rearm-resouces/30-minute-meeting"
            booking.save()
            return redirect(booking.calendly_event_uri)
    else:
        form = DemoBookingForm()
    return render(request, 'book_demo_page.html', {'form': form})

@require_GET
def about(request):
    try:
        about_content = AboutSection.objects.filter(is_active=True).latest('id')
    except AboutSection.DoesNotExist:
        about_content = None
    
    context = {
        'leadership': Leadership.objects.all().order_by('display_order'),
        'about_content': about_content,
        'team_members': TeamMember.objects.filter(
            is_active=True,
            show_on_about=True
        ).order_by('order'),
        'page_name': 'about',
        'meta_title': getattr(about_content, 'meta_title', 'About Us | Your Company'),
        'meta_description': getattr(about_content, 'meta_description', 'Learn about our company and team'),
        'canonical_url': request.build_absolute_uri(request.path)
    }
    return render(request, 'rearm/about.html', context)

def product_list(request):
    context = {
        'agricultural_products': Product.objects.filter(
            product_type='type1', 
            is_active=True
        ).select_related('category'),
        'equipment_products': Product.objects.filter(
            product_type='type2', 
            is_active=True
        ).select_related('category'),
    }
    return render(request, 'rearm/products/list.html', context)

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    context = {
        'product': product,
        'related_products': Product.objects.filter(
            category=product.category,
            is_active=True
        ).exclude(id=product.id)[:4],
    }
    return render(request, 'rearm/products/detail.html', context)