from rest_framework import serializers
from Pos_Main_App.models import Dishes_model, Employe_model, Bill_model, OrderedDish_model, Table_model





# class Dishes_Serializer(serializers.ModelSerializer):
#     class Meta:
#         model = Dishes_model
#         fields = ['id','Dish_Image','Dish_Name','Dish_Quantity','Dish_Price','Dish_Food_Type','Dish_Type','Dish_Information']









class Employe_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Employe_model
        fields = '__all__'

class Dishes_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Dishes_model
        fields = '__all__'






# class OrderedDish_Serializer(serializers.ModelSerializer):
#     dish = Dishes_Serializer(read_only=True)  # Nested serializer for dish details

#     class Meta:
#         model = OrderedDish_model
#         fields = ['dish', 'quantity']

# class Bill_Serializer(serializers.ModelSerializer):
#     employee = Employe_Serializer(read_only=True)  # Nested serializer for employee details
#     dishes = OrderedDish_Serializer(many=True, read_only=True)  # Nested serializer for ordered dishes

#     class Meta:
#         model = Bill_model
#         fields = ['bill_number', 'created_at', 'employee', 'table', 'total_amount', 'dishes']





class Table_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Table_model
        fields = '__all__'



class OrderedDish_Serializer(serializers.ModelSerializer):
    class Meta:
        model = OrderedDish_model
        fields = ['dish', 'quantity']

class Bill_Serializer(serializers.ModelSerializer):
    dishes = OrderedDish_Serializer(many=True, write_only=True)  # Accept dish details in request
    employee = serializers.PrimaryKeyRelatedField(queryset=Employe_model.objects.all(), required=True)
    table = serializers.PrimaryKeyRelatedField(queryset=Table_model.objects.all(), required=False, allow_null=True)

    class Meta:
        model = Bill_model
        fields = ['bill_number', 'created_at', 'employee', 'table', 'total_amount', 'dishes']

    def create(self, validated_data):
        dishes_data = validated_data.pop('dishes')  # Extract ordered dishes
        bill = Bill_model.objects.create(**validated_data)

        total_amount = 0
        for dish_data in dishes_data:
            dish = dish_data['dish']
            quantity = dish_data['quantity']
            OrderedDish_model.objects.create(bill=bill, dish=dish, quantity=quantity)
            total_amount += dish.Dish_Price * quantity  # Assuming `Dish_Price` exists in Dishes_model

        bill.total_amount = total_amount
        bill.save()
        return bill
