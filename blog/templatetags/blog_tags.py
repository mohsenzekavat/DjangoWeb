from django import template
from ..models import Post, Comment
from django.db.models import Count, Max, Min
from markdown import markdown
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User

register = template.Library()


@register.simple_tag()
def total_posts():
    return Post.published.count()


@register.simple_tag()
def total_comments():
    return Post.published.count()


@register.simple_tag()
def last_post_date():
    return Post.published.last().publish


@register.simple_tag
def most_popular_posts(count=5):
    return Post.published.annotate(comments_count=Count('comments')).order_by('-comments_count')[:count]


@register.simple_tag
def most_reading_time():
    return Post.published.annotate(most_reading_time=Max('reading_time')).order_by('-most_reading_time')[:3]


@register.simple_tag
def least_reading_time():
    return Post.published.annotate(least_reading_time=Min('reading_time')).order_by('least_reading_time')[:3]


@register.simple_tag
def most_popular_users(count=2):
    return User.objects.annotate(posts_count=Count('posts')).order_by('-posts_count')[:count]


@register.inclusion_tag('partials/latest_posts.html')
def latest_posts(count=3):
    l_posts = Post.published.order_by('-publish')[:count]
    context = {
        'l_posts': l_posts
    }
    return context


@register.filter(name='markdown')
def to_markdown(text):
    return mark_safe(markdown(text))


@register.filter()
def censorship(text):
    bad_words = ['fuck', 'shit', 'ass', 'cunt']
    for word in bad_words:
        text = text.replace(word, '*' * len(word))
    return mark_safe(text)
