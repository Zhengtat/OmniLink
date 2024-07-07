from django.urls import path
from .views import CreatePurchaseView

app_name = "purchases"

urlpatterns = [
    path('create/', CreatePurchaseView.as_view(), name='create-purchase'),
]