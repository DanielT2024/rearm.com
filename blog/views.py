from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Post, Category, NewsletterSubscriber
from .forms import NewsletterForm, ContactForm
from django.http import JsonResponse
from django.core.paginator import Paginator

def home(request):
    posts = Post.objects.filter(is_published=True).order_by('-created_at')
    featured_posts = Post.objects.filter(is_published=True).order_by('-created_at')[:3]
    recent_posts = Post.objects.filter(is_published=True).order_by('-created_at')[3:6]
    categories = Category.objects.all()
    
    if request.method == 'POST':
        form = NewsletterForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = NewsletterForm()
    
    return render(request, 'blog/post_list.html', {
        'posts': posts,
        'featured_posts': featured_posts,
        'recent_posts': recent_posts,
        'categories': categories,
        'newsletter_form': form
    })

class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 9
    
    def get_queryset(self):
        return Post.objects.filter(is_published=True).order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recent_posts'] = Post.objects.filter(is_published=True).order_by('-created_at')[:5]
        context['categories'] = Category.objects.all()
        context['newsletter_form'] = NewsletterForm()
        return context

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recent_posts'] = Post.objects.filter(is_published=True).exclude(
            id=self.object.id
        ).order_by('-created_at')[:5]
        context['categories'] = Category.objects.all()
        context['newsletter_form'] = NewsletterForm()
        context['contact_form'] = ContactForm()
        return context

def category_posts(request, slug):
    category = get_object_or_404(Category, slug=slug)
    posts = Post.objects.filter(categories=category, is_published=True).order_by('-created_at')
    paginator = Paginator(posts, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'blog/post_list.html', {
        'posts': page_obj,
        'category': category,
        'recent_posts': Post.objects.filter(is_published=True).order_by('-created_at')[:5],
        'categories': Category.objects.all(),
        'newsletter_form': NewsletterForm()
    })

def subscribe_newsletter(request):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        form = NewsletterForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        return JsonResponse({'success': False, 'errors': form.errors})
    return JsonResponse({'success': False, 'errors': 'Invalid request'})

def submit_contact(request):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        return JsonResponse({'success': False, 'errors': form.errors})
    return JsonResponse({'success': False, 'errors': 'Invalid request'})