from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import User,Auction,Comments,wishlist,bids
from django.db.models import Max

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
@login_required
def createlist(request):
    if request.method=="GET":
        return render(request, "auctions/createlist.html")
    else:
        title,StartingBid,des,image,category,uid=request.POST["title"],request.POST["StartingBid"],request.POST["des"],request.POST["image"],request.POST["category"],request.POST["uid"]
        user=User.objects.get(id=uid)
        auction=Auction(title=title,startingBid=float(StartingBid),des=des,image=image,category=category,listedby=user)
        auction.save()
        return HttpResponseRedirect(reverse("index"))

def auctionpage(request,title):
    auction=Auction.objects.get(id=int(title))
    comments=Comments.objects.filter(Auction=auction).all()
    wish=None
    if  not request.user.is_authenticated:
        pass
    else:
        user=User.objects.get(id=request.user.id)
        print(wishlist.objects.filter(auction=auction,user=user).count())
        if(wishlist.objects.filter(auction=auction,user=user).count()>0):
            wish=1
        else:
            wish=0
        
    if request.method=="GET":
        return render(request,"auctions/auction.html",{
            "auction":auction,
            "comments":comments,  
            "wish":wish 
        })
    else:
        
        comment,uid=request.POST["comment"],request.POST["uid"]
        user=User.objects.get(id=uid)
        comment=Comments(user=user,Auction=auction,comment=comment)
        comment.save()
        return render(request,"auctions/auction.html",{
            "auction":auction,
            "comments":comments,
            "wish":wish
        })
@login_required
def bid(request):
    if request.method=="POST":
        bid,uid,title=request.POST["bid"],request.POST["uid"],request.POST["title"]
        auction=Auction.objects.get(id=int(title))
        currentBid=auction.currentBid
        if currentBid != None:
            print("1")
            if(currentBid>float(bid)):
                comments=Comments.objects.filter(Auction=auction).all()
                return render(request,"auctions/auction.html",{
                    "error":"Your bid is lower than the current bid.",
                    "auction":auction,
                    "comments":comments
                })
            else:
                user=User(pk=request.user.id)
                auction.currentBid=float(bid)
                auction.currentbiduser=user
                Bid=bids(user=user,auction=auction,bid=bid)
                Bid.save()
                return HttpResponseRedirect(reverse("auctionpage",kwargs={'title':title}))
        else:
            print("2")
            user=User(pk=request.user.id)
            auction.currentBid=float(bid)
            auction.currentbiduser=user
            Bid=bids(user=user,auction=auction,bid=bid)
            auction.save()
            Bid.save()
            print("4")
            return HttpResponseRedirect(reverse("auctionpage",kwargs={'title':title}))

def category(request):
    return render(request,"auctions/categories.html")

def categoryl(request,cat):
    auctions=Auction.objects.filter(category=cat).all()
    return render(request,"auctions/categoryl.html",{
        "cat":cat,
        "auctions":auctions
    })
@login_required(login_url='/')
def Wishlist(request):
    user=User(pk=request.user.id)
    wishes=user.wishlist.all()
    return render(request,"auctions/wishlist.html",{
        "wishes":wishes
    })
@login_required(login_url='/')
def addwishlist(request,auction):
    title=auction
    auction=Auction.objects.get(id=int(auction))
    user=User(pk=request.user.id)
    if(wishlist.objects.filter(auction=auction,user=user).all().count()==0):
        wish=wishlist(user=user,auction=auction)
        wish.save()
    return HttpResponseRedirect(reverse("auctionpage",kwargs={'title':title}))

def closebid(request,title):
    auction=Auction.objects.get(id=int(title))
    auction.biddingclose=1
    auction.save()
    return HttpResponseRedirect(reverse("auctionpage",kwargs={'title':title}))

def removewish(request,auction):
    title=auction
    auction=Auction.objects.get(id=int(auction))
    wish=wishlist.objects.filter(auction=auction,user=request.user).delete()
    return HttpResponseRedirect(reverse("auctionpage",kwargs={'title':title}))