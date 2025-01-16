from rest_framework.routers import DefaultRouter
from django.urls import path ,include
from .import views
router=DefaultRouter()
router.register(r'list',views.DriverViewset)
router.register(r'reviews',views.ReviewViewset)
urlpatterns = [
    path('',include(router.urls)),
]
