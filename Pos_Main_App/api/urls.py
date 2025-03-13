from django.contrib import admin
from django.urls import path
from Pos_Main_App.api.views import (
    Dishes_View, Dishes_Details_View, Bill_View, Bill_Details_View, 
    Employe_View, Employe_Details_View, OrderDishes_View, orderDishes_Details_View, Table_View, ContactSupportView
)
from . import views
from .views import test_slack_error

urlpatterns = [
    path('Dishes-list/', Dishes_View.as_view(), name='Dishes-list'),
    path('Dishes-list/<int:pk>/', Dishes_Details_View.as_view(), name='Dishes-detail'),

    path('Bill-list/', Bill_View.as_view(), name='Bill-list'),
    path('Bill-list/<int:pk>/', Bill_Details_View.as_view(), name='Bill-detail'),

    path('Employe-list/', Employe_View.as_view(), name='Employe-list'),
    path('Employe-list/<int:pk>/', Employe_Details_View.as_view(), name='Employe-detail-list'),

    path('Order-Dishes-list/', OrderDishes_View.as_view(), name='Order-Dishes-list'),
    path('Order-Dishes-list/<int:pk>/', orderDishes_Details_View.as_view(), name='Order-Dishes-detail'),

    path('Tables/', Table_View.as_view(), name='tables'),
    path('Tables/<int:pk>/', Table_View.as_view(), name='Table-detail'),

    path('data/', views.api_data, name='api_data'),
    path('test-error/', test_slack_error, name='test_slack_error'),
    path('contact-support/', ContactSupportView.as_view(), name='contact-support')
]
