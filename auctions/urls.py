from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("createlist",views.createlist, name="createlist"),
    path("auctionpage/<int:title>",views.auctionpage, name="auctionpage"),
    path("bid",views.bid,name="bid"),
    path("category",views.category,name="category"),
    path("category/<str:cat>",views.categoryl,name="categoryl"),
    path('wishlist',views.Wishlist,name='wishlist'),
    path('addwishlist/<int:auction>',views.addwishlist,name="addwishlist"),
    path('closebid/<int:title>',views.closebid,name="closebid"),
    path('removewish/<int:auction>',views.removewish,name="removewish")
]
