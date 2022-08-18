import yaml
from django.http import JsonResponse

from api.models import Shop, Category, Product, ProductInfo, Parameter, ProductParameter


def uploading_data_to_db(request, path, filename,  ):
    data = _find_file(path, filename)
    shop_id = _create_shop(request, data)
    return _create_product(data, shop_id)


def _find_file(path, filename):
    try:
        with open(path, 'r') as stream:
            try:
                data = yaml.safe_load(stream)
                return data
            except yaml.YAMLError as exc:
                raise exc
    except FileNotFoundError:
        raise f'File {filename} does not exist'


def _create_shop(request, data):
    shop, _ = Shop.objects.get_or_create(name=data['shop'], user_id=request.user.id)
    for category in data['categories']:
        category_object, _ = Category.objects.get_or_create(id=category['id'], name=category['name'])
        category_object.shops.add(shop.id)
        category_object.save()
    ProductInfo.objects.filter(shop_id=shop.id).delete()
    return shop.id


def _create_product(data, shop_id):
    for item in data['goods']:
        product, _ = Product.objects.get_or_create(name=item['name'], category_id=item['category'])
        product_info = ProductInfo.objects.create(product_id=product.id,
                                                  external_id=item['id'],
                                                  model=item['model'],
                                                  price=item['price'],
                                                  price_rrc=item['price_rrc'],
                                                  quantity=item['quantity'],
                                                  shop_id=shop_id)
        for name, value in item['parameters'].items():
            parameter_object, _ = Parameter.objects.get_or_create(name=name)
            ProductParameter.objects.create(product_info_id=product_info.id,
                                            parameter_id=parameter_object.id,
                                            value=value)
    return JsonResponse({'Status': '201'})


