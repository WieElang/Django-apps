from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.db.models import Count 
from .models import Post, Comment, Type
from .forms import PostForm, CommentForm

# Create your views here.
def post_list(request):
    types = Type.objects.all()
    if 'type_tag' in request.GET:
        type_id = request.GET['type_tag']
        posts = Post.objects.filter(post_type__id=type_id, published_date__lte=timezone.now()).order_by('published_date').annotate(count_comments=Count('comments'))
        count_post = posts.count()
    elif 'search' in request.GET:
        search = request.GET['search']
        posts = Post.objects.filter(title__icontains=search, published_date__lte=timezone.now()).order_by('published_date').annotate(count_comments=Count('comments'))
        count_post = posts.count()
    else:
        posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date').annotate(count_comments = Count('comments'))
        count_post = posts.count()
    return render(request, 'blog/post_list.html', {'posts':posts, 'count_post':count_post, 'types':types})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.date = timezone.now()
            comment.save()
    else:
        comment_form = CommentForm()     
    comments = post.comments.all()   
    return render(request, 'blog/post_detail.html', {'post':post, 'comments':comments 'comment_form': comment_form})

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form':form})

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form':form})