from django.contrib import admin
from Pos_Main_App.models import Dishes_model, Employe_model, Bill_model, Table_model, OrderedDish_model

# Register your models here.


class Dishes_admin(admin.ModelAdmin):
    list_display= ['id','Dish_Image','Dish_Name','Dish_Quantity','Dish_Price','Dish_Food_Type','Dish_Type','Dish_Information']
admin.site.register(Dishes_model, Dishes_admin)  




class Employe_admin(admin.ModelAdmin):
    list_display= ['Employe_Name','Employe_Number','Employe_Address','Employe_Position']
admin.site.register(Employe_model, Employe_admin)  





class Bill_admin(admin.ModelAdmin):
    list_display = ['id','bill_number', 'created_at', 'employee', 'total_amount', 'table', 'get_dishes']

    def get_dishes(self, obj):
        return ", ".join([dish.Dish_Name for dish in obj.dishes.all()])
    
    get_dishes.short_description = "Ordered Dishes"

admin.site.register(Bill_model, Bill_admin)



class Table_admin(admin.ModelAdmin):
    list_display= ['Table_Number']
admin.site.register(Table_model, Table_admin) 





class OrderedDish_admin(admin.ModelAdmin):
    list_display= ['bill','dish','quantity']
admin.site.register(OrderedDish_model,OrderedDish_admin) 