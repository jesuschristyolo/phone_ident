from rest_framework import serializers

from .models import UserNumber


# Сериализатор работающий с моделями
class NumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserNumber
        # поля для сериализации. Все поля - __all__
        fields = ('phone_number', 'telecommunication_operator', 'owners_region')


# class NumberSerializer(serializers.Serializer):
#     phone_number = serializers.CharField(max_length=11)
#     telecommunication_operator = serializers.CharField()
#     owners_region = serializers.CharField()
#     time_create = serializers.DateTimeField(read_only=True)
#
#     def create(self, validated_data):
#         return UserNumber.objects.create(**validated_data)
#
#     def update(self, instance, validated_data):
#         instance.phone_number = validated_data.get("phone_number", instance.phone_number)
#         instance.telecommunication_operator = validated_data.get("telecommunication_operator",
#                                                                  instance.telecommunication_operator)
#         instance.owners_region = validated_data.get("owners_region", instance.owners_region)
#         instance.time_create = validated_data.get("time_create", instance.time_create)
#         instance.save()
#         return instance
#




