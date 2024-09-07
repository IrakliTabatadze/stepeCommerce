from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, DetailView, View, DeleteView, UpdateView

from orders.models import Cart, CartItem, Order, OrderItem
from shop.models import Product
from django.urls import reverse_lazy


class OrdersView(TemplateView):
    @staticmethod
    def post(request):
        user = request.user
        cart = get_object_or_404(Cart, user=user)
        cart_items = CartItem.objects.filter(cart=cart)

        if not cart_items:
            return redirect('orders:cart')

        order = Order.objects.create(user=user, cart=cart, total_amount=0)
        total_amount = 0

        for item in cart_items:
            OrderItem.objects.create(order=order, product=item, price=item.product.price, quantity=item.quantity)
            total_amount += item.price * item.quantity

            product = item.product
            product.quantity -= item.quantity

            product.save()
            item.delete()

        order.total_amount += total_amount
        order.save()


class OrderConfirmationView(DetailView):
    model = Order
    template_name = 'orders/order_confirmation.html'
    context_object_name = 'order'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class CartView(TemplateView):
    model = Cart
    template_name = 'orders/cart.html'
    context_object_name = 'cart_items'

    def get_queryset(self):
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        return CartItem.objects.filter(cart=cart)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_items = self.get_queryset()
        total_amount = sum(item.product.price * item.quantity for item in cart_items)
        context['total_amount'] = total_amount

        return context


class AddCartItemView(View):
    @staticmethod
    def post(request, pk):
        product = get_object_or_404(Product, pk=pk)
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item = CartItem.objects.get_or_create(cart=cart, product=product)

        if not created:
            cart_item.quantity += 1
        else:
            cart_item.quantity = 1

        cart_item.save()
        return redirect('orders:cart')


class DeleteCartItemView(DeleteView):
    model = CartItem
    success_url = reverse_lazy('orders:cart')


class UpdateCartItemView(View):
    @staticmethod
    def post(request, pk):
        cart_item = CartItem.objects.get(pk=pk, cart__user=request.user)
        new_quantity = int(request.POST['quantity'])

        if 0 < new_quantity <= cart_item.product.quantity:
            cart_item.quantity = new_quantity
            cart_item.save()
        elif new_quantity <= 0:
            cart_item.delete()

        return redirect('orders:cart')
