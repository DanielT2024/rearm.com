from django.contrib import admin
from django.urls import path, include
from rearm import views
from .views import book_demo_page
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('services/', views.services, name='services'),
    path('services/<slug:slug>/', views.service_detail, name='service_detail'),
    path('book-demo/', book_demo_page, name='book_demo'),
    path('about/', views.about, name='about'),
    path('products/', views.product_list, name='product_list'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    
    # CKEditor 5 upload endpoint (for admin/content editors)
    path('ckeditor5/', include('django_ckeditor_5.urls')),
    
    # Admin panel
    path('admin/', admin.site.urls),
]

# Only serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)