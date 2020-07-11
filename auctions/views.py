from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User,Auction,Comments


def index(request):
    return render(request, "auctions/index.html",{
        "auctions":Auction.objects.all()
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def createlist(request):
    if request.method=="GET":
        return render(request, "auctions/createlist.html")
    else:
        title,StartingBid,des,image,category,uid=request.POST["title"],request.POST["StartingBid"],request.POST["des"],request.POST["image"],request.POST["category"],request.POST["uid"]
        user=User.objects.get(id=uid)
        auction=Auction(title=title,startingBid=float(StartingBid),des=des,image=image,category=category,listedby=user,currentBid=float(StartingBid))
        auction.save()
        return HttpResponseRedirect(reverse("index"))

def auctionpage(request,title):
    if request.method=="GET":
        auction=Auction.objects.get(id=int(title))
        comments=Comments.objects.filter(Auction=auction).all()
        return render(request,"auctions/auction.html",{
            "auction":auction,
            "comments":comments
        })
    else:
        comment,uid=request.POST["comment"],request.POST["uid"]
        auction=Auction.objects.get(id=int(title))
        user=User.objects.get(id=uid)
        comment=Comments(user=user,Auction=auction,comment=comment)
        comment.save()
        comments=Comments.objects.filter(Auction=auction).all()
        return render(request,"auctions/auction.html",{
            "auction":auction,
            "comments":comments
        })

def bid(request):
    if request.method=="POST":
        bid,uid,title=request.POST["bid"],request.POST["uid"],request.POST["title"]
        auction=Auction.objects.get(id=int(title))
        if(auction.currentBid>float(bid)):
            comments=Comments.objects.filter(Auction=auction).all()
            return render(request,"auctions/auction.html",{
                "error":"Your bid is lower than the current bid.",
                "auction":auction,
                "comments":comments
            })
        else:
            auction.currentBid=bid
            auction.latestbid=uid
            auction.save()
            return HttpResponseRedirect(reverse("auctionpage",kwargs={'title':title}))