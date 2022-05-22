from .models import News, Category
from asgiref.sync import sync_to_async


@sync_to_async
def get_news_by_category(category):
    return News.objects.filter(category_id=category, is_published=True).select_related('category')

