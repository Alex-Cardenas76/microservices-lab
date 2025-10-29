from django.db import models
from slugify import slugify
from authors.models import Author
from categories.models import Category

class PostQuerySet(models.QuerySet):
    def published(self):
        return self.filter(status="published")

class Post(models.Model):
    STATUS_CHOICES = (("draft","draft"), ("published","published"))

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    body = models.TextField()
    author = models.ForeignKey(Author, on_delete=models.PROTECT, related_name="posts")
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="posts")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="draft")
    published_at = models.DateTimeField(null=True, blank=True)
    views = models.PositiveIntegerField(default=0)

    objects = PostQuerySet.as_manager()

    class Meta:
        ordering = ["-published_at", "-id"]
        indexes = [models.Index(fields=["slug", "status"])]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    @property
    def excerpt(self):
        return (self.body or "")[:180] + ("..." if len(self.body or "") > 180 else "")
