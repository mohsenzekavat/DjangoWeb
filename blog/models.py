from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from django_resized import ResizedImageField
import os
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.template.defaultfilters import slugify


# Managers
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)


# Create your models here.
class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft',
        PUBLISHED = 'PB', 'Published',
        REJECTED = 'RJ', 'Rejected',

    CATEGORY_CHOICES = (
        ('Technology', 'Technology'),
        ('Programming', 'Programming'),
        ('Artificial Intelligence', 'Artificial Intelligence'),
        ('Sports', 'Sports'),
        ('Politics', 'Politics'),
        ('Economy', 'Economy'),
        ('Entertainment', 'Entertainment'),
        ('Other', 'Other')
    )

    # Relations
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts',
                               related_query_name='posts')
    # Data Fields
    title = models.CharField(max_length=200)
    description = models.TextField()
    slug = models.SlugField(max_length=200)
    # Date fields
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    # Choice fields
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.DRAFT)

    reading_time = models.PositiveIntegerField(default=0)

    category = models.CharField(max_length=25, choices=CATEGORY_CHOICES, default='OTHER')

    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish'])
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.id])

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            # self.slug = self.title.replace(' ', '-')
        super().save(*args, **kwargs)

    # def delete(self, *args, **kwargs):
    #     for img in self.images.all():
    #         storage, path = img.image_file.storage, img.image_file.path
    #         storage.delete(path)
    #     super().delete(*args, **kwargs)


class Ticket(models.Model):
    message = models.TextField()
    name = models.CharField(max_length=250)
    email = models.EmailField()
    phone = models.CharField(max_length=11)
    subject = models.CharField(max_length=250)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=250)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=False)

    class Meta:
        ordering = ['created']
        indexes = [
            models.Index(fields=['created'])
        ]

    def __str__(self):
        return f'{self.name}: {self.post}'


class Image(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images')
    title = models.CharField(max_length=250, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    image_file = ResizedImageField(upload_to=f"blog/post_images/{timezone.now().year}/", size=[500, 500],
                                   quality=75, crop=['middle', 'center'])

    class Meta:
        ordering = ['created']
        indexes = [
            models.Index(fields=['created'])
        ]

    # def delete(self, *args, **kwargs):
    #     storage, path = self.image_file.storage, self.image_file.path
    #     storage.delete(path)
    #     super().delete(*args, **kwargs)

    def __str__(self):
        if self.title:
            return self.title
        if self.image_file and self.image_file.name:
            return self.image_file.name.split('/')[-1]
        return "Unnamed Image"


@receiver(post_delete, sender=Image)
def delete_image_file(sender, instance, **kwargs):
    if instance.image_file:
        instance.image_file.delete(save=False)


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='account')
    date_of_birth = models.DateField(blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    photo = ResizedImageField(upload_to=f"blog/profile_images/{timezone.now().year}/", size=[500, 500], quality=60,
                              crop=['middle', 'center'], blank=True, null=True)
    job = models.CharField(max_length=250, blank=True, null=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Account'
        verbose_name_plural = 'Accounts'
