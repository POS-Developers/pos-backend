from rest_framework import serializers
from Pos_Main_App.models import Dishes_model, Employe_model, Bill_model, Table_model
from django.utils import timezone








class Employe_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Employe_model
        fields = '__all__'

class Dishes_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Dishes_model
        fields = '__all__'



class Table_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Table_model
        fields = '__all__'



# class OrderedDish_Serializer(serializers.ModelSerializer):
#     class Meta:
#         model = OrderedDish_model
#         fields = ['dish', 'quantity']

# class Bill_Serializer(serializers.ModelSerializer):
#     dishes = OrderedDish_Serializer(many=True, write_only=True)  # Accept dish details in request
#     employee = serializers.PrimaryKeyRelatedField(queryset=Employe_model.objects.all(), required=True)
#     table = serializers.PrimaryKeyRelatedField(queryset=Table_model.objects.all(), required=False, allow_null=True)

#     class Meta:
#         model = Bill_model
#         fields = ['bill_number', 'created_at', 'employee', 'table', 'total_amount', 'dishes']

#     def create(self, validated_data):
#         dishes_data = validated_data.pop('dishes')  # Extract ordered dishes
#         bill = Bill_model.objects.create(**validated_data)

#         total_amount = 0
#         for dish_data in dishes_data:
#             dish = dish_data['dish']
#             quantity = dish_data['quantity']
#             OrderedDish_model.objects.create(bill=bill, dish=dish, quantity=quantity)
#             total_amount += dish.Dish_Price * quantity  # Assuming `Dish_Price` exists in Dishes_model

#         bill.total_amount = total_amount
#         bill.save()
#         return bill
# class OrderedDish_Serializer(serializers.ModelSerializer):
#     dish_name = serializers.ReadOnlyField(source='dish.Dish_Name')  # Include dish name in response

#     class Meta:
#         model = OrderedDish_model
#         fields = ['dish', 'quantity', 'dish_name']  # Include dish name in response

# class Bill_Serializer(serializers.ModelSerializer):
#     dishes = OrderedDish_Serializer(many=True, write_only=True)  # Accept dish details in request
#     ordered_dishes = OrderedDish_Serializer(many=True, read_only=True)  # Show ordered dishes in response
#     employee = serializers.PrimaryKeyRelatedField(queryset=Employe_model.objects.all(), required=True)
#     table = serializers.PrimaryKeyRelatedField(queryset=Table_model.objects.all(), required=False, allow_null=True)

#     class Meta:
#         model = Bill_model
#         fields = ['bill_number', 'created_at', 'employee', 'table', 'total_amount', 'dishes', 'ordered_dishes']

#     def create(self, validated_data):
#         dishes_data = validated_data.pop('dishes')
        
#         today = timezone.now().date()
#         last_bill = Bill_model.objects.filter(created_at__date=today).order_by('-bill_number').first()
#         bill_number = last_bill.bill_number + 1 if last_bill else 1
        
#         bill = Bill_model.objects.create(bill_number=bill_number, **validated_data)
        
#         total_amount = 0
#         for dish_data in dishes_data:
#             dish = dish_data['dish']
#             quantity = dish_data['quantity']
#             OrderedDish_model.objects.create(bill=bill, dish=dish, quantity=quantity)
#             total_amount += dish.Dish_Price * quantity
        
#         bill.total_amount = total_amount
#         bill.save()
#         return bill



class Bill_Serializer(serializers.ModelSerializer):
    ordered_dishes = serializers.ListField(
        child=serializers.DictField(),
        allow_empty=True
    )

    class Meta:
        model = Bill_model
        fields = ['id', 'bill_number', 'created_at', 'employee', 'table', 'total_amount', 'ordered_dishes']
        read_only_fields = ['bill_number', 'created_at', 'total_amount']

    def validate_ordered_dishes(self, value):
        """ Validate ordered dishes JSON format """
        for dish in value:
            if not all(key in dish for key in ["dish_id", "name", "quantity", "price"]):
                raise serializers.ValidationError("Each dish must have 'dish_id', 'name', 'quantity', and 'price'.")
            if not isinstance(dish["quantity"], int) or dish["quantity"] <= 0:
                raise serializers.ValidationError("Quantity must be a positive integer.")
            if not isinstance(dish["price"], (int, float)) or dish["price"] < 0:
                raise serializers.ValidationError("Price must be a non-negative number.")
        return value

    def create(self, validated_data):
        """ Automatically calculate total_amount before saving """
        ordered_dishes = validated_data.pop('ordered_dishes', [])
        total_amount = sum(dish["price"] * dish["quantity"] for dish in ordered_dishes)
        bill = Bill_model.objects.create(total_amount=total_amount, ordered_dishes=ordered_dishes, **validated_data)
        return bill

    def update(self, instance, validated_data):
        """ Update bill and recalculate total amount """
        instance.employee = validated_data.get('employee', instance.employee)
        instance.table = validated_data.get('table', instance.table)
        instance.ordered_dishes = validated_data.get('ordered_dishes', instance.ordered_dishes)

        # Recalculate total amount
        instance.total_amount = sum(dish["price"] * dish["quantity"] for dish in instance.ordered_dishes)
        instance.save()
        return instance
