from . import views
from django.urls import path,include
app_name ="travelapp"
urlpatterns = [

    path('',views.index,name='index'),
    path('about/',views.about,name='about'),
    path('call/',views.call,name="call"),
    path('add/',views.addition,name='addition')
]
