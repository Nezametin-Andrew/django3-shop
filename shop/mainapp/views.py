from django.shortcuts import render
from django.http import HttpResponse
from .models import NoteBook, SmartPhone, Category
from django.views.generic import DetailView


def index(request):
    product = NoteBook.objects.all()
    return render(request,
                  'index.html',
                  {
                      "url": "http://localhost:8000/",
                      "product": product
                  })


def test_view(request):
    cat =Category.objects.get_category_for_site_bar()
    return HttpResponse("hello")


def product_page(request):
    return render(request, 'product.html', {"url": "http://localhost:8000/"})


class ProductDetailView(DetailView):

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
