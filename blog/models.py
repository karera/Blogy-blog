from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.urls import reverse
import uuid
from ckeditor.fields import RichTextField
from PIL import Image as Im

class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=100,null=False,unique=True)

    def __str__(self):
        return self.name


class Blog(models.Model):
    choices =[
        ('draft','Draft'),
        ('published', 'Published'),
        
    ]
    title = models.CharField(max_length=200)
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    slug = models.SlugField(max_length=100,null=False,unique_for_date='created_at')
    content = RichTextField()
    created_at = models.DateField(auto_now_add=True)
    updated_at =models.DateField(auto_now=True)
    status  = models.CharField('status', max_length=15, default='Draft',choices=choices )
    image = models.ImageField(upload_to='blog_images/',null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    categories = models.ForeignKey(Category,on_delete= models.SET_NULL,blank=True,null=True)
    class Meta:
        ordering=['-created_at']
        
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('blog-detail',kwargs={'uuid':self.id, 'slug':self.slug})
    
    def save(self, *args, **kwargs):  # new
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    # def image_tag(self):                     
    #     return mark_safe('<img src="/../../media/%s" width="150" height="150" />' % (self.photo))

    # def save(self): # new
    #     super().save()
    #     img = Im.open(self.image.path)
    #     # resize it
    #     if img.height > 300 or img.width > 300:
    #         output_size = (300,300)
    #         img.thumbnail(output_size)
    #         img.save(self.image.path)


class Comment(models.Model):
    CommentPost = models.ForeignKey(Blog , on_delete=models.CASCADE, related_name= 'comments')
    author = models.ForeignKey(User , on_delete=models.CASCADE)
    content = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self' , null=True , blank=True , on_delete=models.CASCADE , related_name='replies')

    class Meta:
        ordering=['-date_posted']

    def __str__(self):
        return str(self.author) + ' comment ' + str(self.content)

    @property
    def children(self):
        return Comment.objects.filter(parent=self).reverse()

    @property
    def is_parent(self):
        if self.parent is None:
            return True
        return False