from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>",views.wikipage,name="wikipage"),
    path("newpage/",views.newpage,name="newpage"),
    path("random/",views.random,name="random"),
    path("edit/<str:title>",views.edit,name="edit"),
    path("search/",views.search,name="search")
]
