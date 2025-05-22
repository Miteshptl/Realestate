from django.urls import path
from . import views

urlpatterns=[
    path("",views.index,name="index"),
    path("about/",views.about,name="about"),
    path("contact/",views.contact,name="contact"),
    path("thank_you/",views.thank_you,name="thank_you"),
    path("upcoming/",views.upcoming,name="upcoming"),
    path("registered/",views.registered,name="registered"),
    path('projectpage/<int:project_id>/', views.projectpage, name='projectpage'),
    path('upcomingdetail/<int:upcoming_project_id>/', views.upcomingdetail, name='upcomingdetail'),
    path('book_appointment/', views.book_appointment, name='book_appointment'),
    path('confirm_appointment/', views.confirm_appointment, name='confirm_appointment'),
    path('success/', views.success, name='success'),
    path('appointments/', views.user_appointments, name='appointments'),
    path('residential/',views.residential,name='residential'),
    path('commercial/', views.commercial, name='commercial'),




    path("signin/", views.signin, name="signin"),
    path("signup/", views.signup, name="signup"),
    path("userlogout/", views.userlogout, name="userlogout"),
    path("request_password_reset/", views.request_password_reset, name="request_password_reset"),
    path("reset_password/", views.reset_password, name="reset_password"),
]