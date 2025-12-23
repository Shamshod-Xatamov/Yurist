import uuid
from django.db import models
from django.urls import reverse
from django.utils.timezone import now
from django.contrib.auth.models import User
from django_ckeditor_5.fields import CKEditor5Field


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"


class BlogPost(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, db_index=True)

    title = models.CharField(max_length=255)
    excerpt = models.TextField(help_text="Qisqa tavsif (Karta yuzida ko'rinadi)")
    content = CKEditor5Field('Content', config_name='extends')

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)  # Null bo'lishi mumkin emas
    tags = models.CharField(max_length=255, blank=True, help_text="Vergul bilan (masalan: sud, biznes)")

    # MUHIM: Rasm majburiy (blank=False, null=False olib tashlandi)
    image = models.ImageField(upload_to='blog/', verbose_name="Muqova Rasmi")

    published_date = models.DateField(default=now)
    read_time = models.IntegerField(default=5)

    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)  # Yangi!

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog_detail', args=[str(self.uuid)])


class Comment(models.Model):
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='comments')
    author_name = models.CharField(max_length=100)
    content = models.TextField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author_name}"