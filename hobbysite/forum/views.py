from django.shortcuts import render
from .models import Post

def threadList(request):
    threads = Post.objects.all()
    return render(request, "thread_list.html", {'threads': threads})

def threadDetail(request, thread_id):
    thread = Post.objects.get(pk=thread_id)
    return render(request, "thread_detail.html", {'thread': thread})