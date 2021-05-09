from django.views import generic
from .models import Post, Category
from .forms import CommentForm, PostForm, CategoryForm
from django.shortcuts import render, get_object_or_404
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, FormView


class PostList(generic.ListView):
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    template_name = 'post_list.html'
    paginate_by = 4


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

def post_detail(request, slug):
    template_name = 'blog/post_detail.html'
    post = get_object_or_404(Post, slug=slug)
    comments = post.comments.filter(active=True)
    new_comment = None
    # Comment posted
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():

            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()

    return render(request, template_name, {'post': post,
                                           'comments': comments,
                                           'new_comment': new_comment,
                                           'comment_form': comment_form})



class PostCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    form_class = PostForm
    model = Post
    extra_context = {'operation': 'Add a new post'}
    success_message = "Your post has been created and awaits publication"


class CategoryCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    form_class = CategoryForm
    model = Category
    extra_context = {'operation': 'Add a new category'}
    success_message = "The category '%(name)s' has been added to the post categories."
