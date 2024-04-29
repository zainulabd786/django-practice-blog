# from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from django.views import View
from .models import Post
from .forms import CommentForm
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

# def starting_page(request):
#     latest_posts = Post.objects.all().order_by('-date')[:3]
#     return render(request, "blog/index.html", { "posts": latest_posts })
class StartingPageView(ListView):
    template_name = "blog/index.html"
    model = Post
    ordering = ["-date"]
    context_object_name = "posts"

    def get_queryset(self):
        queryset = super().get_queryset()
        data = queryset[:3]
        return data

# def posts(request):
#     all_posts = Post.objects.all().order_by('-date')
#     return render(request, "blog/all-posts.html", { "all_posts": all_posts })

class PostsView(ListView):
    template_name = "blog/all-posts.html"
    model = Post
    ordering = ["-date"]
    context_object_name = "all_posts"

# def post_detail(request, slug):
#     identified_post = get_object_or_404(Post, slug=slug)
#     return render(request, "blog/post-detail.html", {"post": identified_post, "tags": identified_post.tag.all()})

class PostDetailView(View):
    template_name = "blog/post-detail.html"
    
    
    def is_stored_post(self, request, post_id):
        stored_posts = request.session.get("stored_posts")
        if stored_posts is None:
            return False
        if post_id in stored_posts:
            return True
        return False

    def get(self, request, slug):
        identified_post = Post.objects.get(slug=slug)
        context = {
            "post": identified_post,
            "tags": identified_post.tag.all(),
            "form": CommentForm(),
            "comments": identified_post.comments.all(),
            "saved_for_later": self.is_stored_post(request, identified_post.id)
        }
        return render(request, self.template_name, context)
    
    def post(self, request, slug):
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = Post.objects.get(slug=slug)
            comment.save()
            return HttpResponseRedirect(reverse("post-detail-page", args=[slug]))
        
        post = Post.objects.get(slug=slug)
        context = {
            "post": post,
            "tags": post.tag.all(),
            "form": form,
            "comments": post.comments.all().order_by("-id")
        }
        return render(request, self.template_name, context)
    
class ReadLaterView(View):
    def get(self, request):
        stored_posts = request.session.get("stored_posts")

        context = {}

        if stored_posts is None or len(stored_posts) == 0:
            context["posts"] = []
            context["has_posts"] = False
        else:
            posts = Post.objects.filter(id__in=stored_posts)
            context["posts"] = posts
            context["has_posts"] = True

        return render(request, "blog/stored-posts.html", context)

    def post(self, request):
        stored_posts = request.session.get("stored_posts")
        if stored_posts is None:
            stored_posts = []

        post_id = int(request.POST["post_id"]);
        if post_id not in stored_posts:
            stored_posts.append(post_id)
        else:
            stored_posts.remove(post_id)

        request.session["stored_posts"] = stored_posts

        return HttpResponseRedirect(reverse("read-later"))
