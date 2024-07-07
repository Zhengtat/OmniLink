from django.urls import path
from .views import ProductListView,ProductCreateView,ProductUpdateView,ProductDeleteView,ProductRelatedView

app_name = "products"

urlpatterns = [
    path('', ProductListView.as_view(), name = 'products'),
    path('create/', ProductCreateView.as_view(), name = 'product-create'),
    path('<int:pk>/update/', ProductUpdateView.as_view(), name='product-update'),
    path('<int:pk>/delete/', ProductDeleteView.as_view(), name='product-delete'),
    path('<int:pk>/related-products/', ProductRelatedView.as_view(), name='related-products'),
]
