from django.contrib.auth.password_validation import validate_password
from django.http import JsonResponse

from rest_framework import viewsets
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import User, ConfirmEmailToken, Contact
from api.serializers import UserSerializer, ContactSerializer

from django.views.generic import TemplateView


class Home(TemplateView):
    template_name = "home.html"


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            if User.password_comparison(request.data['password'], request.data['password_2']):
                if request.data.get('type'):
                    serializer.context['type'] = request.data['type']
                serializer.save()
                return Response({'response': {'status': '201'}})
            return Response({'response': {'Error': 'пароли не совпадают'}})
        else:
            return Response(serializer.errors)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if request.data.get('password'):
            try:
                validate_password(request.data['password'])
            except Exception as password_error:
                error_array = []
                # noinspection PyTypeChecker
                for item in password_error:
                    error_array.append(item)
                return JsonResponse({'Status': False, 'Errors': {'password': error_array}})
            try:
                User.password_comparison(request.data['password'], request.data['password_2'])
            except Exception:
                return JsonResponse({'Status': 400, 'Error': 'пароли не совпадают'})

        serializer.is_valid(raise_exception=True)
        try:
            self.perform_update(serializer)
        except Exception as ex:
            return JsonResponse({f'Result': {ex}})
        return JsonResponse({'Status': 201, 'massage': 'данные успешно изменены'})


class LoginAccount(APIView):
    """
    Класс для авторизации пользователей
    """

    def post(self, request, *args, **kwargs):
        if {'email', 'password'}.issubset(request.data):
            user = User.objects.filter(email=request.data['email'], password=request.data['password']).first()
            if user is not None:
                if user.is_active:
                    token, _ = Token.objects.get_or_create(user=user)
                    return JsonResponse({'Status': True, 'Token': token.key})
            return JsonResponse({'Status': False, 'Errors': 'Не удалось авторизовать'})
        return JsonResponse({'Status': False, 'Errors': 'Не указаны все необходимые аргументы'})


class ConfirmAccountView(APIView):
    """
    Класс для подтверждения почтового адреса
    """

    def post(self, request, *args, **kwargs):
        if {'email', 'token'}.issubset(request.data):
            token = ConfirmEmailToken.objects.filter(user__email=request.data['email'],
                                                     key=request.data['token']).first()
            if token:
                try:
                    token.user.is_active = True
                    token.user.save()
                    token.delete()
                    return JsonResponse({'Status': True})
                except Exception as ex:
                    return JsonResponse({'Error': f'{ex}'})
            else:
                return JsonResponse({'Status': False, 'Errors': 'Неправильно указан токен или email'})

        return JsonResponse({'Status': False, 'Errors': 'Не указаны все необходимые аргументы'})


class ContactViewSet(viewsets.ModelViewSet):
    """
    Класс для работы с контактами
    """
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [IsAuthenticated, ]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            Contact.objects.create(user_id=request.user.id, **serializer.data)
            return JsonResponse({'Status': '201'})
        except Exception as ex:
            return JsonResponse({'Error': f'{ex}'})
