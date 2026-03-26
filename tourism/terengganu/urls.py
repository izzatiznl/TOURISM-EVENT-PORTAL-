from django.urls import path
from . import views 
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path ('',views.homepage,name='homepage'), #ada
    path('packages/', views.packages, name='packages'), #ada
    path('login/', views.login, name='login'), #ada
    path('register/', views.register, name='register'), #ada
    path('search/' , views.search,name='search'), #ada
    
    
    path('homepage2/', views.homepage2, name='homepage2'),
    path('search/' , views.search,name='search'),
    path('packages2/', views.packages2, name='packages2'),

    path('booking/', views.booking, name='booking'), #ada
    path('display/<int:bookingid>/', views.display, name='display'), #ada

    path('homepage/', views.homepage, name='homepage'),
    path('update_profile/', views.update_profile, name='update_profile'),

    path('booking/delete_booking/<str:bookingid>',views.delete_booking,name='delete_booking'), 
    path('review/', views.review, name='review'),

    path('profile/', views.profile, name='profile'),
    path('logout/', views.logout_view, name='logout_view'), #ade

    path('profile/delete_profile/<int:custid>',views.delete_profile,name='delete_profile'),
    path('profile/update/<str:custname>/', views.update_profile, name='update_profile'),
    path('profile/save/<str:custname>/', views.save_profile, name='save_profile'),
    path('profile/<str:custname>/', views.profile, name='profile'), #ade


    path('update_profile/<str:custname>/', views.save_profile, name='save_profile'), 
    path('update_profile/<str:custname>/', views.update_profile, name='update_profile'),
    path('save/<str:custname>/', views.save_profile, name='save_profile'),]