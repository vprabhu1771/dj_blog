from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Category
from .forms import PostForm, CommentForm
from django.db.models import Q

# Create your views here.

def post_list(request):
    query = request.GET.get('q')
    if query:
        posts = Post.objects.filter(Q(title__icontains=query) | Q(tags__name__icontains=query)).distinct()
    else:
        posts = Post.objects.all()
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    comments = post.comments.all()
    new_comment = None

    if request.method == 'POST':
        c_form = CommentForm(request.POST)
        if c_form.is_valid():
            new_comment = c_form.save(commit=False)
            new_comment.post = post
            new_comment.user = request.user
            new_comment.save()
    else:
        c_form = CommentForm()

    return render(request, 'blog/post_detail.html', {
        'post': post,
        'comments': comments,
        'c_form': c_form
    })

def like_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return redirect('post_detail', slug=slug)
