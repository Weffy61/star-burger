from django.http import JsonResponse
from django.templatetags.static import static
from .models import Order, OrderItem
from rest_framework.decorators import api_view
from rest_framework.response import Response


from .models import Product


def banners_list_api(request):
    # FIXME move data to db?
    return JsonResponse([
        {
            'title': 'Burger',
            'src': static('burger.jpg'),
            'text': 'Tasty Burger at your door step',
        },
        {
            'title': 'Spices',
            'src': static('food.jpg'),
            'text': 'All Cuisines',
        },
        {
            'title': 'New York',
            'src': static('tasty.jpg'),
            'text': 'Food is incomplete without a tasty dessert',
        }
    ], safe=False, json_dumps_params={
        'ensure_ascii': False,
        'indent': 4,
    })


def product_list_api(request):
    products = Product.objects.select_related('category').available()

    dumped_products = []
    for product in products:
        dumped_product = {
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'special_status': product.special_status,
            'description': product.description,
            'category': {
                'id': product.category.id,
                'name': product.category.name,
            } if product.category else None,
            'image': product.image.url,
            'restaurant': {
                'id': product.id,
                'name': product.name,
            }
        }
        dumped_products.append(dumped_product)
    return JsonResponse(dumped_products, safe=False, json_dumps_params={
        'ensure_ascii': False,
        'indent': 4,
    })


@api_view(['POST'])
def register_order(request):
    order_details = request.data
    order = Order.objects.create(
        first_name=order_details.get('firstname'),
        last_name=order_details.get('lastname'),
        address=order_details.get('address'),
        phone_number=order_details.get('phonenumber'),
    )

    return Response(
        {
            'products': [{"product": item.product.pk, "quantity": item.quantity} for item
                         in [OrderItem.objects.create(
                            product=Product.objects.get(pk=product.get('product')),
                            order=order,
                            quantity=product.get('quantity')
                            ) for product in order_details.get('products')]],
            "firstname": order.first_name,
            "lastname": order.last_name,
            "phonenumber": f'+{order.phone_number.country_code}{order.phone_number.national_number}',
            "address": order.address
        }
    )

