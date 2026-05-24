from django.shortcuts import render, get_object_or_404
# Create your views here.
from django.http import JsonResponse
from django.views import View
from .models import MenuItem, Cart, CartItem


class HomeView(View):
    template_name = 'home.html'

    def get(self, request):

        items = MenuItem.objects.prefetch_related('flavors')

        cart_count = 0

        cart_id = request.session.get('cart_id')

        if cart_id:
            cart_count = CartItem.objects.filter(cart_id=cart_id).count()

        return render(request, self.template_name, {
            'items': items,
            'cart_count': cart_count
        })


class AddToCartView(View):

    def post(self, request):

        item_id = request.POST.get('item_id')
        flavor_ids = request.POST.getlist('flavors[]')

        item = MenuItem.objects.get(id=item_id)

        cart_id = request.session.get('cart_id')

        if not cart_id:
            cart = Cart.objects.create()
            request.session['cart_id'] = cart.id
        else:
            cart = Cart.objects.get(id=cart_id)

        cart_item = CartItem.objects.create(
            cart=cart,
            item=item
        )

        if flavor_ids:
            count = len(flavor_ids)
            per_flavor_qty = item.quantity // count if count else 0
            flavor_map = {}
            for fid in flavor_ids:
                flavor_map[str(fid)] = per_flavor_qty

            request.session[f'cart_item_{cart_item.id}_split'] = flavor_map

            cart_item.flavors.set(flavor_ids)

        cart_item.save()

        return JsonResponse({
            "status": "success",
            "cart_count": CartItem.objects.filter(cart=cart).count()
        })

class RemoveCartItemView(View):

    def post(self, request):
        item_id = request.POST.get('item_id')
        cart_id = request.session.get('cart_id')
        cart_item = get_object_or_404(CartItem, id=item_id, cart_id=cart_id)
        cart_item.delete()
        cart_count = CartItem.objects.filter(cart_id=cart_id).count()
        return JsonResponse({
            'status': 'success',
            'cart_count': cart_count
        })


class CartView(View):

    template_name = 'cart.html'

    def get(self, request):

        cart_items = []
        cart_id = request.session.get('cart_id')
        flavor_map = {}
        if cart_id:
            cart_items = CartItem.objects.filter(
                cart_id=cart_id
            ).prefetch_related('flavors', 'item')
            for item in cart_items:
                split = request.session.get(
                    f'cart_item_{item.id}_split',
                    {}
                )
                flavor_map[item.id] = split

        total = 0

        for i in cart_items:
            total += i.item.price

        return render(request, self.template_name, {
            'cart_items': cart_items,
            'total': total,
            'flavor_map': flavor_map
        })