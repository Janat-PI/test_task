from django.urls import path

from .views import BillView, BillInfo, ClientInfo

# api/v1/bills/
urlpatterns = [
    path("downloads/", BillView.as_view()),
    path("info/", BillInfo.as_view()),
    path("info/<str:client>/<str:org>", ClientInfo.as_view())
]

# http://127.0.0.1:8000/api/v1/bills/info/client2/OOO Client2Org1
# http://127.0.0.1:8000/api/v1/bills/info/
# http://127.0.0.1:8000/api/v1/bills/downloads/