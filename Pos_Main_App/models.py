from django.db import models
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
import requests
from django.db import transaction

class Dishes_model(models.Model):
    Dishes_Food_Type = [('Chicken', 'Chicken'), ('Mutton', 'Mutton'), ('Veg', 'Veg')]
    Dishes_Type = [('Main Course', 'Main Course'), ('Starter', 'Starter'), ('Sweet', 'Sweet'), ('Cold Drink', 'Cold Drink'), ('Roti', 'Roti')]
    Dishes_Quantity = [('Full', 'Full'), ('Half', 'Half')]

    Dish_Image = models.ImageField(upload_to='Dish_Images/')
    Dish_Name = models.CharField(max_length=100)
    Dish_Quantity = models.CharField(max_length=4, default='Full', choices=Dishes_Quantity)
    Dish_Price = models.PositiveIntegerField()
    Dish_Food_Type = models.CharField(max_length=7, choices=Dishes_Food_Type)
    Dish_Type = models.CharField(max_length=11, choices=Dishes_Type)
    Dish_Information = models.CharField(max_length=100000)

    def __str__(self):
        return self.Dish_Name

class Table_model(models.Model):
    Table_Number = models.PositiveIntegerField()

    def __str__(self):
        return f"Table {self.Table_Number}"

class Employe_model(models.Model):
    Employes_Position = [('waiter', 'waiter'), ('cook', 'cook'), ('Other', 'Other')]

    Employe_Name = models.CharField(max_length=100)
    Employe_Number = models.CharField(max_length=10, unique=True)
    Employe_Address = models.CharField(max_length=1000)
    Employe_Position = models.CharField(max_length=6, choices=Employes_Position)

    def __str__(self):
        return self.Employe_Name

class Bill_model(models.Model):
    bill_number = models.PositiveIntegerField(editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    employee = models.ForeignKey('Employe_model', on_delete=models.SET_NULL, null=True, blank=False, related_name='bills_served')
    table = models.ForeignKey('Table_model', on_delete=models.SET_NULL, null=True, blank=True, related_name='bills')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    ordered_dishes = models.JSONField(default=list)

    def __str__(self):
        return f"Bill {self.bill_number} - {self.created_at}"

    def save(self, *args, **kwargs):
        if not self.pk:  # Only generate a bill number for new bills
            today = timezone.now().date()
            with transaction.atomic():  # Ensures only one process at a time
                last_bill = (
                    Bill_model.objects.filter(created_at__date=today)
                    .select_for_update()
                    .order_by('-bill_number')
                    .first()
                )
                self.bill_number = last_bill.bill_number + 1 if last_bill else 1

        # Calculate total amount based on ordered_dishes
        self.total_amount = sum(dish["price"] * dish["quantity"] for dish in self.ordered_dishes)

        super().save(*args, **kwargs)

class ContactSupport(models.Model):
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    user_message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name

# Signal to send Slack message
@receiver(post_save, sender=ContactSupport)
def send_slack_notification(sender, instance, created, **kwargs):
    if created and hasattr(settings, "SLACK_WEBHOOK_URL"):
        message = (
            f"🎉 *New Contact Request!*\n"
            f"👤 *Name:* {instance.full_name}\n"
            f"📧 *Email:* {instance.email}\n"
            f"📝 *Message:* {instance.user_message}"
        )
        payload = {"text": message}

        try:
            response = requests.post(settings.SLACK_WEBHOOK_URL, json=payload)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Failed to send Slack notification: {e}")
