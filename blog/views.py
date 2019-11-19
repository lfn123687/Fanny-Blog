from django.shortcuts import render, get_object_or_404, render_to_response
from .models import Post, Tag, Category
from django.views.generic import ListView, DetailView
from django.db.models import Q
import re
import markdown


class IndexView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = context.get('paginator')
        page = context.get('page_obj')
        is_paginated = context.get('is_paginated')
        pagination_data = self.pagination_data(paginator, page, is_paginated)
        context.update(pagination_data)
        return context

    def pagination_data(self, paginator, page, is_paginated):
        if not is_paginated:
            return {}
        first = False
        last = False
        left_has_more = False
        right_has_more = False
        left = []
        right = []
        # number of pages number explicitly displayed
        step = 3
        page_num = page.number
        total_pages = paginator.num_pages
        page_range = paginator.page_range

        if page_num==1:
            right = page_range[page_num:min(page_num+step, total_pages)]
            if right[-1] < total_pages-1:
                right_has_more = True
            if right[-1] < total_pages:
                last = True
        elif page_num == total_pages:
            if page_num - step > first+1:
                left_has_more = True
            left = page_range[max(page_num-1-step, 0):page_num-1]
            if left[0]>1:
                first = True
        else:
            left = page_range[max(page_num-step-1, 0):page_num-1]
            right = page_range[page_num:min(page_num+step, total_pages)]
            if left[0]>2:
                left_has_more = True
            if right[-1]<total_pages-1:
                right_has_more = True
            if left[0]>1:
                first = True
            if right[-1]<total_pages:
                last = True

        data = {
            'left':left,
            'right':right,
            'left_has_more':left_has_more,
            'right_has_more':right_has_more,
            'first':first,
            'last':last,
        }
        return data

def about(request):
    return render_to_response('about.html')

def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.body = markdown.markdown(post.body,
                extensions=[
                    'markdown.extensions.extra',
                    'markdown.extensions.codehilite',
                ])
    return render(request, 'blog/detail.html', {'post': post})

"""
class PostDetailView(DetailView):
    model = Post
    template_name='blog/detail.html'
    context_object_name = 'post'

    def get(self, request, *args, **kwargs):
        response = super(PostDetailView, self).get(request, *args, **kwargs)
        self.object.increase_views()
        return response

    def get_object(self, queryset=None):
        post = super().get_object(queryset=None)
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc',
        ])
        post.body = md.convert(post.body)
        m = re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S)
        post.toc = m.group(1) if m is not None else ''
        return post
"""

class ArchiveView(IndexView):
    def get_queryset(self):
        return super(ArchiveView, self).get_queryset().filter(
            created_time__year = self.kwargs.get('year'),
            created_time__month = self.kwargs.get('month'))

class CategoryView(IndexView):
    def get_queryset(self):
        cate = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        return super(CategoryView, self).get_queryset().filter(category=cate)

class TagView(IndexView):
    def get_queryset(self):
        ta = get_object_or_404(Tag, pk=self.kwargs.get('pk'))
        return super(TagView, self).get_queryset().filter(tags=ta)

def search(request):
    q = request.GET.get('q')
    error_msg = ''

    if not q:
        error_msg = "Please input searching keywords."
        return render(request, 'blog/index.html', {'error_msg': error_msg})
    post_list = Post.objects.filter(Q(title__icontains=q) | Q(body__icontains=q))
    return render(request, 'blog/index.html', {'error_msg': error_msg, 'post_list': post_list})