
from django.urls import path
from . import views

urlpatterns = [
    path("",views.HomeView.as_view(),name="homepage"),
    path("stats",views.StatView.as_view(),name="statpage"),
    path("get-names/",views.get_names),
    path("<str:item>/",views.item_single,name="item_single")
]
