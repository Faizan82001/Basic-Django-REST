from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Pizza, Order, Customer
from django.core.exceptions import ValidationError

class PizzaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pizza
        fields = '__all__'


# class OrderDetailSerializer(serializers.Serializer):
#     id = serializers.UUIDField()
#     price = serializers.DecimalField(max_digits=6, decimal_places=2)
#     quantity = serializers.IntegerField()


class OrderSerializer(serializers.ModelSerializer):
    # pizzas = serializers.ListField(child=OrderDetailSerializer(many=True))

    class Meta:
        model = Order
        fields = "__all__"

    def create(self, validated_data):
        # breakpoint()
        pizzas = validated_data['pizzas']
        # self.validate(pizzas)
        # for pizza in pizzas:
            # try:
            #     Pizza.objects.get(pk=pizza['id'])
            # except ValueError:
            #     raise serializers.ValidationError("This pizza does not exist")
            # return pizza['id']
                
        order = Order.objects.create(**validated_data)
        order.pizzas = pizzas
        order.save()
        return order


    def validate(self, data):
        temp = Pizza.objects.all().values_list('id')
        pizza = [str(item[0]) for item in temp]
        data_ids = [str(x['id']) for x in data['pizzas']]
        if set(data_ids).issubset(set(pizza)):
            return data
        else:
            raise serializers.ValidationError({
                'details': "something went wrong"
            })
