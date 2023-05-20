from .views import RegisterAPI
from django.urls import path
from knox import views as knox_views
from .views import LoginAPI ,HomePageAPIView,MyCoursesListAPIView, coursePageAPI, BuyNowAPIView, verifyPaymentAPI
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('register/', RegisterAPI.as_view(), name='register'),
    path('login/', LoginAPI.as_view(), name='login'),
    path('logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),

    path('home/', HomePageAPIView.as_view(), name='home-page'),
    path('my-courses/', MyCoursesListAPIView.as_view(), name='my-courses-api'),
    path('course/<slug:slug>/', coursePageAPI, name='course-page-api'),
    path('buynow/<slug:slug>/', BuyNowAPIView.as_view(), name='buy-now'),
    path('verify-payment/', verifyPaymentAPI, name='verify-payment-api'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)