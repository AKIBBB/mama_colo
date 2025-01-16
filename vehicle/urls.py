from  django.urls import path ,include
from rest_framework import routers
from .import views

router=routers.DefaultRouter()
router.register('',views.RideRequestViewset)
urlpatterns = [
    path('',include(router.urls)),
    path('ride_requests/', views.RideRequestListCreateAPIView.as_view(), name='ride_requests'),
    path('ride_requests/<int:pk>/accept/', views.AcceptRideRequestAPIView.as_view(), name='accept_ride_request'),
]
