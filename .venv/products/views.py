from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from leads.models import Product 
from django.urls import reverse
from .forms import ProductModelForm

class ProductListView(LoginRequiredMixin, generic.ListView):
    template_name = "products/product_list.html"

    def get_queryset(self):
        return Product.objects.all()

class ProductCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = 'products/product_create.html'
    form_class = ProductModelForm

    def get_success_url(self):
        return reverse("products:products")
    
class ProductUpdateView(LoginRequiredMixin,generic.UpdateView):
    template_name = "products/product_update.html"
    form_class = ProductModelForm
    
    def get_success_url(self):
        return reverse("products:products")

    def get_queryset(self):
        return Product.objects.all()
    
class ProductDeleteView(LoginRequiredMixin,generic.DeleteView):
    template_name = 'products/product_delete.html'
    context_object_name = "product"

    def get_queryset(self):
        return Product.objects.all()
        
    def get_success_url(self):
        return reverse("products:products")