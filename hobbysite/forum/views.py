from django.shortcuts import render
from .models import Post

def threadList(request):
    threads = Post.objects.all().order_by('category__name', '-createdOn')
    return render(request, "threadList.html", {'threads': threads})

def threadDetail(request, threadId):
    thread = Post.objects.get(pk=threadId)
    return render(request, "threadDetail.html", {'thread': thread})