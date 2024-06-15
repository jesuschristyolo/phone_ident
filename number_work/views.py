import rest_framework.generics
from django.forms import model_to_dict
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import status
from django.shortcuts import render
import requests
from rest_framework.views import APIView
from .models import UserNumber
from rest_framework.response import Response

from .serializers import NumberSerializer

url = 'https://opendata.digital.gov.ru/api/v1/abcdef/phone'


# class SecondNumberAPIView(rest_framework.generics.ListAPIView):
#     queryset = UserNumber.objects.all()
#     serializer_class = NumberSerializer


# ListCreateAPI реализует добавление по пост запросу и возврат элем по гет запросу
class NumberAPIList(rest_framework.generics.ListCreateAPIView):
    queryset = UserNumber.objects.all()
    serializer_class = NumberSerializer


class AllNumbersAPIView(APIView):

    def post(self, request):
        serializer = NumberSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'your_data': serializer.data})

    def get(self, request):
        # возвращаем json строку
        lst = UserNumber.objects.all().values()
        return Response({'numbers': list(lst)})

    def put(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)
        if not pk:
            return Response({"error": "Method PUT is not allowed"})
        try:
            instance = UserNumber.objects.get(pk=pk)
        except:
            return Response({"error": "Object does not exists"})

        serializer = NumberSerializer(data=request.data, instance=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'put': serializer.data})


class NumberAPIView(APIView):

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('search_phone', openapi.IN_QUERY, description="Phone number to search",
                              type=openapi.TYPE_STRING)
        ],
        responses={
            status.HTTP_200_OK: openapi.Response(
                description="Successful response",
                examples={
                    "application/json": {
                        "success": True,
                        "phone": "79122894892",
                        "phone_region": "Some Region",
                        "phone_operator": "Some Operator"
                    }
                }
            ),
            status.HTTP_400_BAD_REQUEST: openapi.Response(
                description="Invalid input"
            )
        }
    )
    def get(self, request, *args, **kwargs):

        if request.query_params.get('search_phone'):

            user_phone = list(request.query_params.get('search_phone'))

            for char in user_phone:
                if user_phone.index(char) == 0:
                    if char == '8':
                        user_phone[0] = '7'
                if char in [' ', '-', '+', '(', ')']:
                    user_phone[user_phone.index(char)] = ""

            user_phone = "".join(user_phone)

            print(user_phone)

            response = requests.get(url, params={'num': user_phone, 'limit': 50}, verify=False)
            print(response.json())

            try:
                if len(response.json()['data']) > 1:
                    return Response({'success': False,
                                     'error_description': 'По вашему запросу было выявлено больше 1 номера.'
                                                          ' Проверьте корректность запрашиваемого номера'})
                elif len(response.json()['data']) == 1:
                    phone_region = response.json()['data'][0]['region']
                    phone_operator = response.json()['data'][0]['operator']

                    return Response(
                        {'success': True, 'phone': user_phone, 'phone_region': phone_region,
                         'phone_operator': phone_operator})

                elif len(response.json()['data']) == 0:
                    return Response({'success': False,
                                     'error_description': 'По вашему запросу не было найдено записей.'
                                                          ' Проверьте корректность запрашиваемого номера'})
            except:
                return Response({'success': False,
                                 'error_description': 'Ошибка ввода номера, проверьте корректность'
                                                      ' вводимого номера.'})

        else:
            return Response({'success': False})


def number_identification(request):
    if request.method == 'POST':
        print(request.POST['phone'])
        user_phone = request.POST['phone']
        params = {
            'num': user_phone,
            'limit': 50
        }

        response = requests.get(url, params=params, verify=False)
        print(response.json())

        if len(response.json()['data']) > 1:
            return render(request, template_name='number_work/number_identification.html',
                          context={'exists': 'many'})

        elif len(response.json()['data']) == 1:
            user_region = response.json()['data'][0]['region']
            user_telecommunication_operator = response.json()['data'][0]['operator']

            if not UserNumber.objects.filter(phone_number=user_phone).exists():
                UserNumber.objects.create(phone_number=user_phone, owners_region=user_region,
                                          telecommunication_operator=user_telecommunication_operator)

            new_number = UserNumber.objects.get(phone_number=user_phone)
            return render(request, template_name='number_work/number_identification.html',
                          context={'new_number': new_number, 'exists': 'correct'})

        else:
            return render(request, template_name='number_work/number_identification.html',
                          context={'exists': 'nothing'})

    return render(request, template_name='number_work/number_identification.html')
