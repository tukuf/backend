from django.contrib.auth.models import AbstractUser
from django.db import models

# Custom User model
class User(AbstractUser):
    USER_TYPE_CHOICES = [
        ('landowner', 'Landowner'),
        ('agent', 'Agent'),
        ('buyer', 'Buyer'),
    ]
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    phone = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return f"{self.username}"

# Land model
class Land(models.Model):
    LAND_TYPE_CHOICES = [
        ('residential', 'Residential'),
        ('agricultural', 'Agricultural'),
        ('commercial', 'Commercial'),
        ('industrial', 'Industrial'),
    ]
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owned_lands", limit_choices_to={'user_type': 'landowner'})
    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=255)
    size = models.DecimalField(max_digits=10, decimal_places=2, help_text="Size must be in cm²")
    length = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text="Length must be in meters")
    width = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text="Width must be in meters")
    land_type = models.CharField(max_length=20, choices=LAND_TYPE_CHOICES)
    price = models.DecimalField(max_digits=12, decimal_places=2, help_text="In Tsh")
    image = models.ImageField(upload_to='land_images/', blank=True, null=True)
    listed_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listed_lands", limit_choices_to={'user_type': 'agent'})
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title}"


# Inquiry model
class Inquiry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'user_type': 'buyer'})
    land = models.ForeignKey(Land, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Inquiry by {self.user.username} on {self.land.title}"


# Transaction model
class Transaction(models.Model):
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'user_type': 'buyer'})
    agent = models.ForeignKey(User, on_delete=models.CASCADE, related_name="handled_transactions", limit_choices_to={'user_type': 'agent'})
    land = models.ForeignKey(Land, on_delete=models.CASCADE)
    transaction_date = models.DateTimeField(auto_now_add=True)
    final_price = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"Transaction: {self.buyer.username} bought {self.land.title}"


# Review model
class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'user_type': 'buyer'})
    land = models.ForeignKey(Land, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField()  # Rating out of 5
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.username} - {self.rating} stars"


# Notification model
class Notification(models.Model):
    recipient = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.recipient.username} - {'Read' if self.is_read else 'Unread'}"
