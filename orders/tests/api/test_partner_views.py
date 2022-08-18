import pytest

from .fixtures import URL, client, user_factory, shop_factory, category_factory, product_factory, \
    product_info_factory, parameter_factory, product_parameter_factory, order_factory, contact_factory, \
    order_item_factory


@pytest.mark.django_db
def test_partner_state(client, user_factory, shop_factory):
    user = user_factory(_quantity=1, type='shop')[0]
    shop = shop_factory(_quantity=1, user_id=user.pk)[0]

    client.force_authenticate(user=user)

    get_user_data = client.get(f"{URL}user/{user.pk}/").json()
    assert get_user_data['type'] == 'shop'

    url_state = f"{URL}partner/state/"
    post_state = client.put(url_state, data={'name': shop.name, 'state': 'True'}).json()
    assert post_state['Status'] == True

    get_state = client.get(f"{url_state}").json()
    assert get_state['Shop state'] == shop.state


@pytest.mark.django_db
def test_partner_order(client, user_factory, shop_factory, category_factory, product_factory,
                       product_info_factory, parameter_factory, product_parameter_factory,
                       order_factory, contact_factory, order_item_factory):
    user_shop = user_factory(_quantity=1, **{'type': 'shop'})[0]
    shop = shop_factory(_quantity=1, **{'user_id': user_shop.pk})[0]
    category = category_factory(_quantity=1, make_m2m=True)[0]
    category.shops.set((shop,))
    product = product_factory(_quantity=1, **{'category_id': category.pk})[0]
    product_info = product_info_factory(_quantity=1, **{'shop_id': shop.pk, 'product_id': product.pk})[0]
    parameter = parameter_factory(_quantity=1)[0]
    product_parameter_factory(_quantity=1, **{'product_info_id': product_info.pk,
                                              'parameter_id': parameter.pk})
    buyer = user_factory(_quantity=1)[0]
    contact = contact_factory(_quantity=1, **{'user_id': buyer.pk})[0]
    order = order_factory(_quantity=1, **{'user_id': buyer.pk, 'contact_id': contact.pk,
                                          'product_id': product.pk, 'state': 'basket'})[0]
    order_item_factory(_quantity=1, **{'order_id': order.pk,
                                       'product_info_id': product_info.pk})

    client.force_authenticate(user=user_shop)

    url = f'{URL}orders/'
    get_response = client.get(url).json()

    assert get_response['Data']
    assert len(get_response['Data']) == 1
