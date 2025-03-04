from rest_framework import serializers
from Pos_Main_App.models import (
    Dishes_model, Employe_model, Bill_model,
    OrderedDish_model, Table_model,ContactSupport
)

class Dishes_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Dishes_model
        fields = '__all__'

class Employe_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Employe_model
        fields = '__all__'

class Table_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Table_model
        fields = '__all__'

class OrderedDish_Serializer(serializers.ModelSerializer):
    class Meta:
        model = OrderedDish_model
        fields = ['dish', 'quantity']

class Bill_Serializer(serializers.ModelSerializer):
    dishes = OrderedDish_Serializer(many=True, write_only=True)
    employee = serializers.PrimaryKeyRelatedField(queryset=Employe_model.objects.all())
    table = serializers.PrimaryKeyRelatedField(queryset=Table_model.objects.all(), required=False, allow_null=True)
    
    class Meta:
        model = Bill_model
        fields = ['bill_number', 'created_at', 'employee', 'table', 'total_amount', 'dishes']

    def create(self, validated_data):
        dishes_data = validated_data.pop('dishes')
        bill = Bill_model.objects.create(**validated_data)
        total_amount = 0
        for dish_data in dishes_data:
            dish = dish_data['dish']
            quantity = dish_data['quantity']
            OrderedDish_model.objects.create(bill=bill, dish=dish, quantity=quantity)
            total_amount += dish.Dish_Price * quantity  # Assumes 'Dish_Price' exists
        bill.total_amount = total_amount
        bill.save()
        return bill


class ContactSupportSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactSupport
        fields = '__all__'