from django.contrib import admin
from .models import Post, Tag, Category
from django.forms import Textarea
from django.db import models

class PostAdmin(admin.ModelAdmin):
    list_display=['title', 'created_time', 'modified_time', 'category', 'author']
    fields=['title', 'body', 'excerpt', 'category', 'tags']
    formfield_overrides = {
        models.TextField:{'widget': Textarea(attrs={'rows':60, 'cols':140})},
    }

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        super().save_model(request, obj, form, change)

admin.site.register(Post, PostAdmin)
admin.site.register(Category)
admin.site.register(Tag)