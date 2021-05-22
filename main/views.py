from django.http import HttpResponseRedirect
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView


class IndexView(TemplateView):
    """トップページ"""
    template_name = 'main/index.html'