from django.urls import path, include, re_path
from django_rest_passwordreset.views import reset_password_request_token, reset_password_confirm
from rest_framework.routers import DefaultRouter

from .views.order_views import BasketView, OrderView
from .views.partner_views import PartnerUpdate, PartnerState, PartnerOrders
from .views.product_views import CategoryView, ShopView, ProductInfoView
from .views.user_views import LoginAccount, ConfirmAccountView, UserViewSet, ContactViewSet

app_name = 'api'

router = DefaultRouter()
router.register('user', UserViewSet, basename='users')
router.register('contact', ContactViewSet, basename='contacts')

urlpatterns = [
    path('', include(router.urls)),
    path('login/', LoginAccount.as_view(), name='login'),
    path('confirm/', ConfirmAccountView.as_view(), name='confirm-post'),
    path('partner/update/', PartnerUpdate.as_view(), name='partner-update'),
    path('partner/state/', PartnerState.as_view(), name='partner-state'),
    path('orders/', PartnerOrders.as_view(), name='partner-get-orders'),
    path('categories/', CategoryView.as_view(), name='categories'),
    path('shops/', ShopView.as_view(), name='shops'),
    path('products/', ProductInfoView.as_view(), name='products'),
    path('basket/', BasketView.as_view(), name='basket'),
    path('order/', OrderView.as_view(), name='order'),
    path('user/password_reset/', reset_password_request_token, name='password-reset'),
    path('user/password_reset/confirm/', reset_password_confirm, name='password-reset-confirm'),
]
