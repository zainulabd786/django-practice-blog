from django.db import models
from datetime import date
from django.urls import reverse;
from django.core.validators import MinLengthValidator
# from django.utils.text import slugify

class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.full_name()
    
class Tag(models.Model):
    caption = models.CharField(max_length=100)

    def __str__(self):
        return self.caption

class Post(models.Model):
    title = models.CharField(max_length=255)
    excerpt = models.TextField(max_length=300)
    image = models.ImageField(upload_to="posts", null=True)
    date = models.DateField(auto_now=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=False)
    content = models.TextField(validators=[MinLengthValidator(10)])
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, related_name='posts', null=True)
    tag = models.ManyToManyField(Tag)

    def get_absolute_url(self):
            """
            Returns the absolute URL for the current instance.
            The URL is generated using the 'post-detail-page' view and the instance's slug.
            """
            return reverse('post-detail-page', args=[self.slug])

    def __str__(self):
        return self.title
