from .models import News, Category
from asgiref.sync import sync_to_async


@sync_to_async
def get_posts_by_category(category):
    return News.objects.filter(category_id=category, is_published=True).select_related('category')


@sync_to_async()
def get_all_categories():
    return Category.objects.all()
