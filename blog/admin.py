from django.contrib import admin
from .models import Post,Comment

# Register your models here.

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    '''Admin View for Post'''

    list_display = ('title','slug','author','publish','status')
    list_filter = ('created_at','publish','author','status')
    raw_id_fields = ('author',)
    readonly_fields = ('created_at','updated_at')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title','body')
    date_hierarchy = 'publish'
    ordering = ('status','publish')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    '''Admin View for Comment'''

    list_display = ('name','email','post','created_at','active')
    list_filter = ('created_at','active')
    search_fields = ('name','email','body')
   


    
