from django.contrib import admin

from .models import Category, Location, Post, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Административная панель для модели Post."""

    list_display = (
        'title',
        'text',
        'pub_date',
        'created_at',
        'is_published',
        'author',
        'location',
        'category',
    )
    list_editable = (
        'text',
        'location',
        'category',
    )
    search_fields = ('title', 'author',)
    list_filter = ('category', 'location',)
    list_display_links = ('title',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Административная панель для модели Category."""

    list_display = (
        'title',
        'is_published',
    )
    list_editable = ('is_published',)
    search_fields = ('title',)
    list_filter = ('is_published',)


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    """Административная панель для модели Location."""

    list_display = (
        'name',
        'is_published',
    )
    list_editable = ('is_published',)
    search_fields = ('name',)
    list_filter = ('is_published',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Административная панель для модели Comment."""

    list_display = (
        'id',
        'post',
        'author',
        'text',
        'created_at',
    )
    list_editable = (
        'text',
    )
    search_fields = (
        'text',
        'author__username',
        'post__title',
    )
    list_filter = (
        'post',
        'author',
        'created_at',
    )
    list_display_links = ('id',)

    def save_model(self, request, obj, form, change):
        if not obj.author_id:
            obj.author = request.user
        super().save_model(request, obj, form, change)
