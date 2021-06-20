# import json
# import urllib.request
# import urllib.parse
from django.conf import settings
# from django.contrib import messages
from django.views import generic
from .models import Post, Category
from .forms import CommentForm, PostForm, CategoryForm
from django.shortcuts import render, get_object_or_404
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from django.urls import reverse

class PostList(generic.ListView):
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    template_name = 'post_list.html'
    paginate_by = 4


class PostDetailView(generic.DetailView):
    model = Post
    template_name = 'blog/post_detail.html'

    #Copied from xtdcomments
    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        context.update({'next': reverse('comments-xtd-sent')})
        return context

    # def get_context_data(self, **kwargs):
    #     context = super(PostDetailView, self).get_context_data(**kwargs)
    #     context['post'] = 'English word detail view'
    #     return context


class CategoryList(generic.ListView):
    queryset = Category.objects.all().order_by('name')
    template_name = 'category_list.html'
    paginate_by = 10


# class PostDetail(generic.DetailView):
#     model = Post
#     template_name = 'blog/post_detail.html'
def category_detail(request, pk):
    template_name = 'blog/category_detail.html'
    category = get_object_or_404(Category, id=pk)
    posts = category.posts.all()
    return render(request, template_name, {'category': category,
                                           'posts': posts})

# def post_detail(request, slug):
#     template_name = 'blog/post_detail.html'
#     post = get_object_or_404(Post, slug=slug)
#     comments = post.comments.filter(active=True)
#     new_comment = None
#     # Comment posted
#     if request.method == 'POST':
#         comment_form = CommentForm(data=request.POST)
#         if comment_form.is_valid():
#             ''' Begin reCAPTCHA validation '''
#             recaptcha_response = request.POST.get('g-recaptcha-response')
#             url = 'https://www.google.com/recaptcha/api/siteverify'
#             values = {
#                 'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
#                 'response': recaptcha_response
#             }
#             data = urllib.parse.urlencode(values).encode()
#             req =  urllib.request.Request(url, data=data)
#             response = urllib.request.urlopen(req)
#             result = json.loads(response.read().decode())
#             ''' End reCAPTCHA validation '''

#             if result['success']:
#                 # Create Comment object but don't save to database yet
#                 new_comment = comment_form.save(commit=False)
#                 # Assign the current post to the comment
#                 new_comment.post = post
#                 # Save the comment to the database
#                 new_comment.save()
#                 # messages.success(request, 'New comment added with success!')
#             else:
#                 messages.error(request, 'Invalid reCAPTCHA. Please try again.')
#     else:
#         comment_form = CommentForm()

#     return render(request, template_name, {'post': post,
#                                            'comments': comments,
#                                            'new_comment': new_comment,
#                                            'comment_form': comment_form})



class PostCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    form_class = PostForm
    model = Post
    extra_context = {'operation': 'Add a new post'}
    success_message = "Your post has been created and awaits publication."

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class CategoryCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    form_class = CategoryForm
    model = Category
    extra_context = {'operation': 'Add a new category'}
    success_message = "The category '%(name)s' has been added to the post categories."

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
