from django.shortcuts import render,redirect,get_object_or_404,HttpResponseRedirect
from django.http import HttpResponse
from .forms import NewUserForm,BlogForm,CommentForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from . models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger



def home(request):
   posts = Blog.objects.all()
   context = (
        {"posts" : posts}
    )
   return render(request, 'blog/index.html',context)

def about(request):
    return render(request, 'blog/category.html')



def blog(request):
    posts = Blog.objects.all().order_by('-created_at')
    cate = Category.objects.all()
    paginator = Paginator(posts, 2)
    page = request.GET.get('page')

     # 6 employees per page


    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        # if page is not an integer, deliver the first page
        page_obj = paginator.page(1)
    except EmptyPage:
        # if the page is out of range, deliver the last page
        page_obj = paginator.page(paginator.num_pages)
    
    context = {
        "posts" : posts,
        "cate" : cate,
        "page":page,
        'paginator':paginator,
        'page_obj': page_obj
    }

    return render(request, 'blog/blog.html',context)


def singles(request,slug,uuid):
    data = get_object_or_404(Blog, slug=slug, id=uuid)
    comment_form = CommentForm()
    comments = data.comments.all()
    new_comment = None
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form .is_valid():
            new_comment = comment_form .save(commit=False)
            new_comment.user = request.user
            new_comment.data= data
            new_comment.save()
            # return redirect(data.get_absolute_url()+'#'+str(new_comment.id))
        else:
            comment_form  = CommentForm()
    context = {
        "data": data,
        "comment_form ":comment_form,
        'new_comment': new_comment,
        'comments': comments,
    }
    return render(request, 'blog/single.html', context)


# def postComment(request):
#     if request.method == 'POST':
#         comment = request.POST.get('comment')
#         user = request.user
#         comment = Comment(comment=comment,user=user)
#         comment.save()
#         messages.success(request,'Your comment has been posted successfully')
#     return redirect('/blog/{data.slug}')

@login_required
def create(request):
    if request.method == 'POST':
        form = BlogForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            # post.author = request.user
            post.save()
            return redirect('blog-home')
    else:
        form = BlogForm()
    context = {'form': form}
    return render(request, 'blog/create.html', context)


@login_required
def update_post(request,slug ,uuid):
   
    obj = Blog.objects.get( slug=slug, id=uuid)
    form = BlogForm(instance =obj)
    if request.method == 'POST':
        form = BlogForm( request.POST,request.FILES, instance =obj)
        if form.is_valid():
            form.save()
            return redirect('blog-bloges')
    context = {
        'form': form,
        'obj':obj
    }
    return render(request, 'blog/update_view.html', context)


@login_required
def delete(request,slug ,uuid):
   
    obj = Blog.objects.get( slug=slug, id=uuid)
    if request.method == 'POST':
        obj.delete()
        return redirect('blog-bloges')
      
    context = {
        'obj':obj
    }
    return render(request, 'blog/delete.html', context) 