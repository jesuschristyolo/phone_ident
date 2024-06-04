from rest_framework import serializers

from .models import UserNumber


# Сериализатор работающий с моделями
class NumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserNumber
        # поля для сериализации. Все поля - __all__
        fields = ('phone_number', 'telecommunication_operator', 'owners_region')


class NumberModel:

    def __init__(self, phone_number, telecommunication_operator, owners_region):
        self.phone_number = phone_number
        self.telecommunication_operator = telecommunication_operator
        self.owners_region = owners_region








