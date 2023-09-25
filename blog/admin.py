from django.contrib import admin
from . models import Blog,Category,Comment

# Register your models here.
class Blogadmin(admin.ModelAdmin):
    list_display = ('title', 'content')
    prepopulated_fields = {"slug": ("title",)}

class Categoryadmin(admin.ModelAdmin):
    # list_display = ('title', 'content')
    prepopulated_fields = {"slug": ("name",)}

admin.site.register(Blog,Blogadmin)
admin.site.register(Category,Categoryadmin)
admin.site.register(Comment)