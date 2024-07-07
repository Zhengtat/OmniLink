from django.shortcuts import render
from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from agents.mixins import OrganisorAndLoginRequiredMixin
from leads.models import Product, Lead, Agent, Purchase
from django.urls import reverse
from .forms import CreatePurchaseForm

# Create your views here.
class CreatePurchaseView(LoginRequiredMixin, generic.CreateView):
    template_name = "purchases/create_purchase.html"
    form_class = CreatePurchaseForm

    def get_form_kwargs(self, **kwargs):
        kwargs = super(CreatePurchaseView, self).get_form_kwargs(**kwargs)
        kwargs.update ({
            "request": self.request
        })
        return kwargs
    
    def get_success_url(self):
        return reverse("agents:agents")
    
    def form_valid(self,form):
        purchase = form.save(commit = False)
        leads = form.cleaned_data["lead"]
        products = form.cleaned_data["product"]
        agents = Agent.objects.get(id = self.request.user.id)
        purchase.lead = leads
        purchase.product = products
        purchase.agent = agents
        return super(CreatePurchaseView,self).form_valid(form)