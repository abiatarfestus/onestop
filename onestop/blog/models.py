from django.db import models
from django.conf import settings
from django.urls import reverse
from django_extensions.db.fields import AutoSlugField
from django.contrib.auth.models import User
from django_resized import ResizedImageField
# from django_comments.moderation import CommentModerator
# from django_comments_xtd.moderation import moderator


STATUS = (
    (0, "Draft"),
    (1, "Publish")
)


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post_categories')

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        #from django.urls import reverse
        return reverse('blog:category-detail', args=[str(self.id)])


class Post(models.Model):
    title = models.CharField(max_length=255, unique=True)
    slug = AutoSlugField(populate_from=['title'], unique=True)
    category = models.ManyToManyField(
        Category, related_name='posts', default='Uncategorised')
    image = ResizedImageField(
        verbose_name='featured image', quality=100, upload_to='featured_image/%Y/%m/', blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    updated_on = models.DateTimeField(auto_now=True)
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        #from django.urls import reverse
        return reverse('blog:post-detail', args=[str(self.slug)])


class Comment(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField(verbose_name='comment')
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return 'Comment {} by {}'.format(self.body, self.name)

# class PostCommentModerator(CommentModerator):
#     email_notification = True
#     auto_moderate_field = 'publish'
#     moderate_after = 365


# moderator.register(Post, PostCommentModerator)