from django.contrib import admin


# Register your models here.
from .models import Auction,Comments,bids,User

class AuctionAdmin(admin.ModelAdmin):
    list_display=("__str__","currentBid","startingBid")


admin.site.register(Auction,AuctionAdmin)
admin.site.register(Comments)
admin.site.register(bids)
admin.site.register(User)