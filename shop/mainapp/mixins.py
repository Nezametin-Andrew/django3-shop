from django.views.generic.detail import SingleObjectMixin

from .models import Category


class CategoryDetailMixin(SingleObjectMixin):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = Category.objects.get_category_for_site_bar()
        context['url'] = "http://localhost:8000/"
        return context
