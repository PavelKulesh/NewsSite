from django.urls import path

from news.views import *

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('', HomeNews.as_view(), name='home'),
    path('category/<int:category_id>/', NewsByCategory.as_view(), name='category'),
    path('news/<int:pk>/', ViewNews.as_view(), name='view_news'),
    path('news/add-news/', CreateNews.as_view(), name='add_news'),
    path('news/update-news/<int:pk>/', UpdateNews.as_view(), name='update_news'),
    path('news/delete-news/<int:pk>/', DeleteNews.as_view(), name='delete_news'),
]
