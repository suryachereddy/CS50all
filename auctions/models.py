from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Auction(models.Model):
    listedby=models.ForeignKey(User,on_delete=models.CASCADE,related_name="auctions")
    image=models.CharField(max_length=512,null=True)
    startingBid=models.FloatField()
    currentBid=models.FloatField(default=100.00)
    category=models.CharField(max_length=64,default="other")
    title=models.CharField(max_length=64,default="Title")
    des=models.CharField(max_length=256,default="No Description.")
    date=models.DateTimeField(auto_now=True)
    latestbid=models.IntegerField(null=True)

class Comments(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="comments")
    Auction=models.ForeignKey(Auction,on_delete=models.CASCADE,related_name="comments")
    comment=models.CharField(max_length=512)

