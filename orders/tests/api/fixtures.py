import pytest
from model_bakery import baker
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from api.models import User, Shop, Contact, ConfirmEmailToken, Order, Product, ProductInfo, Parameter, ProductParameter, \
    OrderItem, Category

URL = 'http://127.0.0.1:8000/api/v1/'


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def user_factory():
    def factory(*args, **kwargs):
        return baker.make(User, *args, **kwargs)
    return factory


@pytest.fixture
def shop_factory():
    def factory(*args, **kwargs):
        return baker.make(Shop, *args, **kwargs)
    return factory


@pytest.fixture
def contact_factory():
    def factory(*args, **kwargs):
        return baker.make(Contact, *args, **kwargs)
    return factory


@pytest.fixture
def confirm_email_token_factory():
    def factory(*args, **kwargs):
        return baker.make(ConfirmEmailToken, *args, **kwargs)
    return factory


@pytest.fixture
def category_factory():
    def factory(*args, **kwargs):
        return baker.make(Category, *args, **kwargs)
    return factory


@pytest.fixture
def product_factory():
    def factory(*args, **kwargs):
        return baker.make(Product, *args, **kwargs)
    return factory


@pytest.fixture
def product_info_factory():
    def factory(*args, **kwargs):
        return baker.make(ProductInfo, *args, **kwargs)
    return factory


@pytest.fixture
def parameter_factory():
    def factory(*args, **kwargs):
        return baker.make(Parameter, *args, **kwargs)
    return factory


@pytest.fixture
def product_parameter_factory():
    def factory(*args, **kwargs):
        return baker.make(ProductParameter, *args, **kwargs)
    return factory


@pytest.fixture
def order_factory():
    def factory(*args, **kwargs):
        return baker.make(Order, *args, **kwargs)
    return factory


@pytest.fixture
def order_item_factory():
    def factory(*args, **kwargs):
        return baker.make(OrderItem, *args, **kwargs)
    return factory
