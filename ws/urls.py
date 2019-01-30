from ws import views
from django.urls import path
from rest_framework import routers
from ws.views import BusStatusViewSet

router = routers.DefaultRouter()
router.register(r'busstatuses', BusStatusViewSet)

app_name = 'busapi'
urlpatterns = [
    # 書籍
    path('v1/busstatuses', views.busstatus_list, name='busstatus_list'),
]
