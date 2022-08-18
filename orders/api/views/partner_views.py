import os
from distutils.util import strtobool

from django.conf import settings
from django.db.models import Sum, F
from django.http import JsonResponse

from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.models import Shop, Order
from api.permissions import IsShop
from api.serializers import OrderSerializer, ShopSerializer
from api.views.supporotive.supportive_for_partner import uploading_data_to_db

from rest_framework.throttling import UserRateThrottle


class PartnerUpdate(CreateAPIView):
    """
    Класс для обновления прайса от поставщика
    """
    permission_classes = (IsAuthenticated, IsShop)
    throttle_scope = 'update_price'

    def post(self, request, *args, **kwargs):
        query = request.data
        filename = query['file']
        directory = query['folder']
        path_to_file = f'{settings.BASE_DIR}/{directory}/{filename}'
        if os.path.exists(path_to_file):
            return uploading_data_to_db(request, path_to_file, filename)
        return JsonResponse({'Status': False, 'Errors': 'Не указаны все необходимые аргументы'})


class PartnerState(RetrieveUpdateAPIView):
    """
    Класс для работы со статусом поставщика
    """
    permission_classes = (IsAuthenticated, IsShop,)
    serializer_class = ShopSerializer

    def put(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            try:
                Shop.objects.filter(user_id=request.user.id).update(state=strtobool(request.data.get('state')))
                return JsonResponse({'Status': True})
            except ValueError as error:
                return JsonResponse({'Status': False, 'Errors': str(error)})
        return JsonResponse({'Status': False, 'Errors': 'Не указаны все необходимые аргументы'})

    def get(self, request, *args, **kwargs):
        get_shop = Shop.objects.filter(user_id=request.user.id).first()
        if get_shop.state:
            return JsonResponse({'Response': '200', 'Shop state': get_shop.state})
        return JsonResponse({'Response': 'Нет доступа'})


class PartnerOrders(RetrieveAPIView):
    """
    Класс для получения заказов поставщиками
    """
    permission_classes = (IsAuthenticated, IsShop, UserRateThrottle,)
    serializer_class = OrderSerializer

    def get(self, request, *args, **kwargs):
        try:
            order = Order.objects.filter(
                ordered_items__product_info__shop__user_id=request.user.id, state='basket').prefetch_related(
                'ordered_items__product_info__product__category',
                'ordered_items__product_info__product_parameters__parameter').select_related('contact').annotate(
                total_sum=Sum(F('ordered_items__quantity') * F('ordered_items__product_info__price'))).distinct()
            serializer = self.get_serializer(order, many=True, )
            return JsonResponse({'Data': serializer.data})
        except Exception as ex:
            return JsonResponse({'Error': f'{ex}'})
