from django.conf import settings
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Post, Group, User
from .forms import PostForm
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required


def index(request):
    post_list = Post.objects.all()
    paginator = Paginator(post_list, settings.PAGINATOR_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    template = 'posts/index.html'
    title = 'Последние обновления на сайте'

    context = {
        'page_obj': page_obj,
        'title': title,
    }
    return render(request, template, context)


def group_posts(request, slug):
    template = 'posts/group_list.html'
    group = get_object_or_404(Group, slug=slug)
    post_list = group.posts.all()
    paginator = Paginator(post_list, settings.PAGINATOR_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'group': group,
               'page_obj': page_obj,
               }
    return render(request, template, context)


def profile(request, username):
    profile = get_object_or_404(User, username=username)
    profile_posts = profile.posts.all()
    paginator = Paginator(profile_posts, settings.PAGINATOR_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'author': profile,
               'page_obj': page_obj
               }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    author_posts = post.author.posts
    if request.user == post.author:
        is_edit = True
        context = {'post': post,
                   'author_posts': author_posts,
                   'is_edit': is_edit,
                   }
        return render(request, 'posts/post_detail.html', context)
    context = {'post': post,
               'author_posts': author_posts,
               }
    return render(request, 'posts/post_detail.html', context)


@login_required
def post_create(request):
    if request.method != 'POST':
        form = PostForm()
        return render(request, 'posts/create_post.html', {'form': form})
    form = PostForm(request.POST)
    if not form.is_valid():
        return render(request, 'posts/create_post.html', {'form': form})
    form = form.save(commit=False)
    form.author = request.user
    form.save()
    return redirect('posts:profile', form.author)


def post_edit(request, post_id):
    if request.method != 'POST':
        post = get_object_or_404(Post, pk=post_id)
        is_edit = True
        form = PostForm(instance=post)
        author = post.author
        context = {'title': post,
                   'is_edit': is_edit,
                   'form': form}
        if request.user != author:
            template = reverse('posts:post_detail', args=[post_id])
            return redirect(template)
        return render(request, 'posts/create_post.html', context)
    post = get_object_or_404(Post, id=post_id)
    form = PostForm(request.POST, instance=post)
    if not form.is_valid():
        return render(request, 'posts/create_post.html')
    form.save()
    template = reverse('posts:post_detail', args=[post_id])
    return redirect(template)
