from django.urls import path
from superstocks.api.views import api_detail_retailer_view
from superstocks.api.views import login_view
api_name = 'retailer'

urlpatterns = [
    path('<Retailer_id>/', api_detail_retailer_view, name="detail"),
    path('login',login_view, name = "login"),
]
