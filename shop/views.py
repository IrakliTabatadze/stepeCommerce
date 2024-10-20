from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render
from django.views.generic import TemplateView, DetailView
from shop.models import Product, Category
from django.db.models import Q


class AboutUsView(TemplateView):
    template_name = 'shop/about.html'
from collections import defaultdict
from django.db.models import Q

from itertools import groupby
from django.db.models import Q

class ProductView(TemplateView):
    template_name = 'shop/index.html'

    def get(self, request, *args, **kwargs):
        query = request.GET.get('query')
        selected_categories = request.GET.getlist('category')  # List of selected category IDs

        products = Product.objects.all()

        if query:
            products = products.filter(Q(name__icontains=query) | Q(category__name__icontains=query)).distinct()

        if selected_categories:
            products = products.filter(category__in=selected_categories).distinct()

        # Paginate the filtered products
        paginator = Paginator(products, 9)


        page_number = request.GET.get('page')

        try:
            products = paginator.page(page_number)
        except PageNotAnInteger:
            products = paginator.page(1)
        except EmptyPage:
            products = paginator.page(paginator.num_pages)

        # Fetch all categories and group by category_type
        categories = Category.objects.all().order_by('category_type')
        categories_by_type = {}
        for category in categories:
            category_type = category.category_type
            if category_type not in categories_by_type:
                categories_by_type[category_type] = []
            categories_by_type[category_type].append(category)

        return render(request, self.template_name, {
            'products': products,
            'categories_by_type': categories_by_type,  # Grouped categories by type
            'selected_categories': selected_categories,  # Pass selected categories for pre-checking
        })



class ProductDetailView(DetailView):
    template_name = 'shop/detail.html'
    model = Product
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.object
        # Fetch related products from the same categories, excluding the current product
        related_products = Product.objects.filter(
            category__in=product.category.all()
        ).exclude(id=product.id).distinct()[:4]
        context['related_products'] = related_products
        return context
