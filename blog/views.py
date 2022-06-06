from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Post, BlogComment
from django.contrib import messages
from blog.templatetags import extras
# Create your views here.


def blogHome(request):
    allPost = Post.objects.all()
    context = {'allPost': allPost}
    return render(request, 'blog/bloghome.html', context)


def blogPost(request, slug):
    post = Post.objects.filter(slug=slug).first()
    comments = BlogComment.objects.filter(post=post, parent=None)
    replies = BlogComment.objects.filter(post=post).exclude(parent=None)
    replyDict = {}

    for reply in replies:
        if reply.parent.sno not in replyDict.keys():
            replyDict[reply.parent.sno] = [reply]
        else:
            replyDict[reply.parent.sno].append(reply)

    context = {'post': post, 'comments': comments, 'count': len(comments), 'replyDict': replyDict}
    return render(request, 'blog/blogpost.html', context)


def postComment(request):
    if request.method == 'POST':
        comment = request.POST.get('comment')
        postSno = request.POST.get('postSno')
        parentSno = request.POST.get('parentSno')
        post = Post.objects.get(sno=postSno)
        user = request.user

        if parentSno == "":
            comment = BlogComment(user=user, post=post, comment=comment)
            comment.save()
            messages.success(request, 'You comment has been posted.')
            return redirect(f'/blog/{post.slug}')
        else:
            parent = BlogComment.objects.get(sno=parentSno)
            comment = BlogComment(user=user, post=post, comment=comment, parent=parent)
            comment.save()
            messages.success(request, 'You reply has been posted.')
            return redirect(f'/blog/{post.slug}')