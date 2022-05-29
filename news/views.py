import asyncio
import logging
from typing import Dict, Any

from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from news.async_requests import get_news_by_category
from news.forms import NewsForm, UserRegisterForm, UserLoginForm
from news.models import News, Category
from django.contrib import messages

logger = logging.getLogger('django')


class RegisterView(CreateView):
    form_class = UserRegisterForm
    success_url = reverse_lazy('login')
    template_name = 'news/register.html'


class LoginView(View):
    form_class = UserLoginForm
    template_name = 'news/login.html'

    def post(self, request):
        logger.info(request)
        form = self.form_class(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
        else:
            return render(request, self.template_name, {'form': form})

    def get(self, request):
        logger.info(request)
        form = self.form_class()
        return render(request, self.template_name, {'form': form})


class LogoutView(View):
    def get(self, request):
        logger.info(request)
        logout(request)
        return redirect('login')


class HomeNews(ListView):
    model = News
    template_name = 'news/home_news_list.html'
    context_object_name = 'news'
    paginate_by = 2

    def get_queryset(self)->Any:
        return News.objects.filter(is_published=True).select_related('category')


class NewsByCategory(ListView):
    model = News
    template_name = 'news/home_news_list.html'
    context_object_name = 'news'
    paginate_by = 2

    def get_context_data(self, *, object_list=None, **kwargs)-> Dict[str,Any] :
        context = super().get_context_data(**kwargs)
        context['title'] = Category.objects.get(pk=self.kwargs['category_id'])
        return context

    def get_queryset(self):
        coroutine = get_news_by_category(self.kwargs['category_id'])
        return asyncio.run(coroutine)


class ViewNews(DetailView):
    model = News
    context_object_name = 'news_item'


class CreateNews(LoginRequiredMixin, CreateView):
    form_class = NewsForm
    template_name = 'news/add_news.html'
    raise_exception = True

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.author = self.request.user
        obj.save()
        return super(CreateNews, self).form_valid(form)


class UpdateNews(LoginRequiredMixin, UpdateView):
    model = News
    form_class = NewsForm
    template_name = 'news/update_news.html'

    def get_object(self, queryset=None):
        obj = super(UpdateNews, self).get_object(queryset)
        if obj.author != self.request.user:
            messages.error(self.request, "You can't edit this post")
            logger.error("Attempt to get an access to update function")
            raise Http404("You don't own this object")
        return obj


class DeleteNews(LoginRequiredMixin, DeleteView):
    model = News
    template_name = 'news/delete_news.html'

    def get_success_url(self):
        return reverse('home')

    def get_object(self, queryset=None):
        obj = super(DeleteNews, self).get_object(queryset)
        if obj.author != self.request.user:
            messages.error(self.request, "You can't edit this post")
            logger.error("Attempt to get an access to delete function")
            raise Http404("You don't own this object")
        return obj
