from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.home, name = "home"),
    path('login/', views.loginpage, name = "login"),
    path('signup/', views.signup, name = "sign_up"),  
    path('verify_email/<slug:username>', views.verify_email, name = "verify_email"),
    path('user/', views.user_home, name = "user"),   
    path("resend-otp", views.resend_otp, name="resend-otp"),
    path('fetch_details/', views.fetch_details, name='fetch_details'),
    path('user/logout',views.logoutuser),
    path('dashboard', views.dashboard),
    path('social-auth/', include('social_django.urls', namespace='social')),
    path('oauth/', include('social_django.urls', namespace='social')), 
    path('user/upload/', views.upload_image, name='upload_image'),
    path('handle-upload/',views.handle_upload, name="handle_upload"),
    path('sendmail',views.sendmail, name = 'sendmail'),
    path('sendmail2',views.sendmail2, name = 'sendmail2'),
    path('get-user-images-and-predictions/', views.get_user_images, name='get_user_images_and_predictions'),
]