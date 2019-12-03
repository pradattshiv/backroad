from django.urls import path,include
from superstocks.views import *

from rest_framework import routers

router = routers.DefaultRouter()
router.register('', SuperstockistViewSet)

urlpatterns = [
    path('superstocks/', include(router.urls)),
]