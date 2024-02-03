from django.urls import path
from .views import IndexView,SigninView, LoginView,LogOut,CartView,CheckOutView,ordersView,Company
from django.conf import settings
from django.conf.urls.static import static
from Ecom import settings
from .auth import authMiddleware
urlpatterns = [
   path('',IndexView.as_view(),name='index'),
   path('signin',SigninView.as_view(),name='signin'),
   path('login', LoginView.as_view(),name='login'),
   path('logout', LogOut,name='logout'),
   path('cart', CartView.as_view(),name='cart'),
   path('checkout', CheckOutView.as_view(),name='checkout'),
   path('orders/', authMiddleware(ordersView.as_view()), name='orders'),
   path('company/', authMiddleware(Company.as_view()), name='company'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

