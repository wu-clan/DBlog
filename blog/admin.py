from django.contrib import admin

# Register your models here.


from blog.models import Tag, Article, Category,Comment


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    date_hierarchy = 'date_time'
    list_display = (
        'title',
        'category',
        'date_time',
        'content',
        'digest',
        'author',
        'view',
        'comment',
        'picture'
    )
    list_filter = ('category', 'author')
    filter_horizontal = ('tag',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'created_time',
        'last_mod_time'
    )


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'source_id',
        'create_time',
        'user_name',
        'url',
        'comment'
    )