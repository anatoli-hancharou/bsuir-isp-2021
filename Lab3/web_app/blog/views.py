import logging

from django.contrib import messages
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .models import Post, Category


class BlogListView(ListView):
    paginate_by = 2
    model = Post
    template_name = 'home.html'

    queryset = Post.objects.order_by('-publication_date')

    # def get_context_data(self, **kwargs):
    #     context = super(BlogListView, self).get_context_data(**kwargs)
    #     context['object_list'] = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    #     return context
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_categories'] = Category.objects.all()
        return context
    #queryset = Book.objects.filter(publisher__name='Acme Publishing')


class CategoryPostList(ListView):
    paginate_by = 2
    template_name = 'posts_by_category.html'

    def get_queryset(self):
        return Post.objects.filter(categories__title=self.kwargs['category'])


class BlogDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'


class BlogCreateView(CreateView):
    model = Post
    template_name = 'post_new.html'
    fields = ['title', 'body', 'categories']

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.author = self.request.user
        obj.save()
        return super(BlogCreateView, self).form_valid(form)


class BlogUpdateView(UpdateView):
    model = Post
    template_name = 'post_edit.html'
    fields = ['title', 'body', 'categories']

    def get_object(self, queryset=None):
        obj = super(BlogUpdateView, self).get_object(queryset)
        if obj.author != self.request.user:
            messages.error(self.request, "You can't edit this post")
            raise Http404("You don't own this object")
        return obj


class BlogDeleteView(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('home')

    def get_object(self, queryset=None):
        obj = super(BlogDeleteView, self).get_object(queryset)
        if obj.author != self.request.user:
            messages.error(self.request, "You can't edit this post")
            raise Http404("You don't own this object")
        return obj


