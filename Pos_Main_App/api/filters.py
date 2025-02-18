# import django_filters
# from Pos_Main_App.models import Dishes_model, Bill_model, Employe_model,Table_model,OrderedDish_model 




# class Dishes_filter(django_filters.FilterSet):
#     class Meta:
#         model= Dishes_model
#         fields= {
#             'Dish_Name': ['icontains','istartswith'],
#         }



# class Bill_filter(django_filters.FilterSet):
#     class Meta:
#         model = Bill_model
#         fields = {
#             'bill_number': ['exact'],  # Filter by bill number
#             'created_at': ['exact', 'gte', 'lte'],  # Filter by date range
#             'total_amount': ['exact', 'gte', 'lte'],  # Filter by amount range
#             'customer_name': ['icontains'],  # Case-insensitive search
#         }



# class Employe_filter(django_filters.FilterSet):
#     class Meta:
#         model= Employe_model
#         fields= {
#             'Employe_Name': ['icontains','istartswith'],
#         }



# class Table_filter(django_filters.FilterSet):
#     class Meta:
#         model= Table_model
#         fields= {
#             'Table_Number': ['exact'],
#         }



# class OrderedDish_filter(django_filters.FilterSet):
#     class Meta:
#         model= OrderedDish_model
#         fields= {
#             'bill__bill_number': ['exact'],
#         }



import django_filters
from Pos_Main_App.models import Dishes_model, Bill_model, Employe_model, Table_model, OrderedDish_model

class Dishes_filter(django_filters.FilterSet):
     Dish_Type = django_filters.ChoiceFilter(field_name="Dish_Type", choices=Dishes_model.Dishes_Type)  # Exact match for type
     Dish_Name = django_filters.CharFilter(field_name="Dish_Name", lookup_expr="icontains")  # Search box for name
     Dish_Food_Type=django_filters.ChoiceFilter(field_name="Dish_Food_Type", choices=Dishes_model.Dishes_Food_Type)
     
     class Meta:
        model = Dishes_model
        
        fields = ["Dish_Name", "Dish_Type","Dish_Food_Type"]



        

class Bill_filter(django_filters.FilterSet):
    class Meta:
        model = Bill_model
        fields = {
            'bill_number': ['exact'],  # Filter by bill number
            'created_at': ['exact', 'gte', 'lte'],  # Filter by date range
            'total_amount': ['exact', 'gte', 'lte'],  # Filter by amount range
             # Case-insensitive search
        }

class Employe_filter(django_filters.FilterSet):
    class Meta:
        model = Employe_model
        fields = {
            'Employe_Name': ['icontains', 'istartswith'],
            'Employe_Position': ['exact'],
        }

class Table_filter(django_filters.FilterSet):
    Table_Number = django_filters.NumberFilter(field_name="Table_Number", lookup_expr="exact")

    class Meta:
        model = Table_model
        fields = ["Table_Number"]  # Ensure "Table_Number" exists in your Table_model


class OrderedDish_filter(django_filters.FilterSet):
    class Meta:
        model = OrderedDish_model
        fields = {
            'bill__bill_number': ['exact'],  # Use string reference for the relationship
        }


