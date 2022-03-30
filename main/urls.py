
from django.urls import path
from .views  import HomePage , CycleItemsViews, ListItem ,UserRegistrationView ,UserLoginView , UserProfileView
#,UserRegistrationView ,ListItem  

#, , , UserProfileView
# from django.conf.urls import url 
from django.urls import re_path as url

from rest_framework_simplejwt.views import TokenObtainPairView , TokenRefreshView #,TokenVerifyView

urlpatterns = [
	path('' , HomePage , name="home"),
	path('items/', CycleItemsViews.as_view() ),
	path('items/<str:id>', CycleItemsViews.as_view() ),
	path('list/' , ListItem.as_view()) ,
	# path('api/user/' , UserViewer.as_view()),
	url(r'^signup', UserRegistrationView.as_view()),
	url(r'^signin', UserLoginView.as_view()),
	#path('signin', UserLoginView.as_view()),
	url(r'^profile', UserProfileView.as_view()),


	path('token/' , TokenObtainPairView.as_view() , name ='token'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    #path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
	
]

# $ curl -X POST -H "Content-Type: application/json" http://127.0.0.1:8000/api/cart-items/ -d "{\"product_name\":\"name\",\"product_price\":\"41\",\"product_quantity\":\"1\"}"