from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Auction(models.Model):
    listedby=models.ForeignKey(User,on_delete=models.CASCADE,related_name="auctions")
    image=models.CharField(max_length=512,null=True)
    startingBid=models.FloatField()
    category=models.CharField(max_length=64,default="other")
    title=models.CharField(max_length=64,default="Title")
    des=models.CharField(max_length=256,default="No Description.")
    date=models.DateTimeField(auto_now=True)
    biddingclose=models.IntegerField(default=0)
    currentbiduser=models.ForeignKey(User,on_delete=models.CASCADE,related_name="bid",null=True)
    currentBid=models.FloatField(null=True)
    def __str__(self):
        return f"{self.title} is listed by {self.listedby}" 
class Comments(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="comments")
    Auction=models.ForeignKey(Auction,on_delete=models.CASCADE,related_name="comments")
    comment=models.CharField(max_length=512)
    def __str__(self):
        return f"{self.user} commented {self.comment} on {self.Auction.title}" 
class wishlist(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="wishlist")
    auction=models.ForeignKey(Auction,on_delete=models.CASCADE)

class bids(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE, related_name="bids")
    auction=models.ForeignKey(Auction,on_delete=models.CASCADE,related_name="bids")
    bid=models.FloatField(default=1.00)
    def __str__(self):
        return f"{self.user} bidded an amount of ${self.bid} on {self.auction}" 