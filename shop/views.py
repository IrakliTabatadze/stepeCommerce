from django.core.paginator import Paginator
from django.shortcuts import render
from django.views.generic import TemplateView, DetailView
from shop.models import Product
from django.db.models import Q


class ProductView(TemplateView):
    template_name = 'shop/index.html'

    def get(self, request, *args, **kwargs):

        query = request.GET.get('query')

        if query:
            products = Product.objects.filter(Q(name__icontains=query) | Q(category__name__icontains=query))
        else:
            products = Product.objects.all()

        paginator = Paginator(products, 10)
        page_number = request.GET.get('page')
        products = paginator.page(page_number)

        return render(request, self.template_name, {'products': products})


class ProductDetailView(DetailView):
    template_name = 'shop/detail.html'
    model = Product
    context_object_name = 'product'
