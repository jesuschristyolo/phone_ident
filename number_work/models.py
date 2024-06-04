from django.db import models


class UserNumber(models.Model):
    phone_number = models.CharField(max_length=30)
    telecommunication_operator = models.CharField(max_length=100)
    owners_region = models.CharField(max_length=100)
    time_create = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Номер: {self.phone_number}, Оператор: {self.telecommunication_operator}, Регион: {self.owners_region}"




