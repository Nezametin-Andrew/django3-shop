from django.shortcuts import render
from django.http import HttpResponse
from .models import NoteBook, SmartPhone, Category
from django.views.generic import DetailView, View

from .mixins import CategoryDetailMixin


class BaseView(View):

    def get(self, request, *args, **kwargs):
        context = {
            "category": Category.objects.get_category_for_site_bar()
        }
        return render(request, 'index.html', context)


class ProductDetailView(CategoryDetailMixin, DetailView):

    CT_MODEL_MODEL_CLASS = {
        'notebook': NoteBook,
        'smartphone': SmartPhone
    }

    def dispatch(self, request, *args, **kwargs):
        self.model = self.CT_MODEL_MODEL_CLASS[kwargs['ct_model']]
        self.queryset = self.model._base_manager.all()
        return super().dispatch(request, *args, **kwargs)

    context_object_name = "product"

    template_name = "product_detail.html"
    pk_url_kwarg = "id"


class CategoryDetailView(CategoryDetailMixin, DetailView):
    model = Category
    queryset = Category.objects.all()
    context_object_name = 'category_name'
    template_name = 'category_detail.html'
    slug_url_kwarg = 'slug'

