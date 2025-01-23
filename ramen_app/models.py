from django.db import models
from django.contrib.auth.models import User

class RamenShop(models.Model):
    name = models.CharField(max_length=255)
    url = models.URLField(null=True, blank=True)
    features = models.TextField(null=True, blank=True)
    distance_from_station = models.CharField(max_length=255, null=True, blank=True)
    category = models.CharField(max_length=255, null=True, blank=True)
    dinner_price = models.CharField(max_length=255, null=True, blank=True)
    lunch_price = models.CharField(max_length=255, null=True, blank=True)
    payment_method = models.CharField(max_length=255, null=True, blank=True)
    image_url = models.URLField(null=True, blank=True)  # 新しいフィールド

    def __str__(self):
        return self.name

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ramen_shop = models.ForeignKey(RamenShop, related_name='reviews',on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, f'{i} stars') for i in range(1, 6)])
    comment = models.TextField()
    def __str__(self):
        return f'{self.user.username} - {self.ramen_shop.name}'

class Likes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ramen_shop = models.ForeignKey(RamenShop, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('user', 'ramen_shop')
