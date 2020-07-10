from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Auction(models.Model):
    listedby=models.ForeignKey(User,on_delete=models.CASCADE,related_name="auctions")
    image=models.CharField(max_length=512,null=True)
    startingBid=models.FloatField()
    currentBid=models.IntegerField(null=True)
    category=models.CharField(max_length=64)
    title=models.CharField(max_length=64)
    des=models.CharField(max_length=256)

class Comments(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="comments")
    Auction=models.ForeignKey(Auction,on_delete=models.CASCADE,related_name="comments")
    comment=models.CharField(max_length=512)

