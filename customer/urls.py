from rest_framework.routers import DefaultRouter
from django.urls import path ,include
from .import views
from .views import activate

router=DefaultRouter()
router.register(r'list',views.CustomerViewset)
urlpatterns = [
    path('',include(router.urls)),
    path('active/<uid64>/<token>', activate, name='active'),
    path('register/',views.UserReApiViewgistration.as_view(),name='register'),
    path('login/', views.UserLoginApiView.as_view(), name='login'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path('profile/',views.CustomerProfileAPIView.as_view(),name='profile'),
]
