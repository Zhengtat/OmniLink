from typing import Any
from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView, FormView
from .models import Lead, Agent, Category, Purchase
from .forms import LeadForm, LeadModelForm, CustomedUserCreationForm, AssignAgentForm, LeadCategoryUpdateForm
from django.core.mail import send_mail
from django.contrib.auth.mixins import LoginRequiredMixin
from agents.mixins import OrganisorAndLoginRequiredMixin
import datetime

# Create your views here.
class LandingPageView(LoginRequiredMixin, TemplateView):
    template_name = 'landing.html'

class LeadListView(LoginRequiredMixin, ListView):
    template_name = "leads/lead_list.html"
    context_object_name = "leads"

    def get_queryset(self):
        user = self.request.user
        #initial query set of leads for tiktok
        if user.is_organisor:
            queryset = Lead.objects.filter(organisation = user.userprofile, agent__isnull = False)
        else:
            queryset = Lead.objects.filter(organisation = user.agent.organisation, agent__isnull = False)
            #filter by sales person
            queryset = queryset.filter(agent__user = user)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super(LeadListView, self).get_context_data(**kwargs)
        user = self.request.user
        if user.is_organisor:
            queryset = Lead.objects.filter(organisation = user.userprofile, agent__isnull = True)
            context.update({
                "unassigned_leads": queryset
            })
        return context

class LeadDetailView(LoginRequiredMixin, DetailView):
    template_name = "leads/lead_detail.html"
    context_object_name = "lead"
    def get_queryset(self):
        user = self.request.user
        #initial query set of leads for tiktok
        if user.is_organisor:
            queryset = Lead.objects.filter(organisation = user.userprofile)
        else:
            queryset = Lead.objects.filter(organisation = user.agent.organisation)
            #filter by sales person
            queryset = queryset.filter(agent__user = user)
        return queryset

class LeadCreateView(LoginRequiredMixin, CreateView):
    template_name = "leads/lead_create.html"
    form_class = LeadModelForm

    def get_success_url(self):
        return reverse("leads:lead-list")
    
    def form_valid(self,form):
        lead = form.save(commit = False)
        lead.organisation = self.request.user.userprofile
        send_mail(
            subject = "A lead has been created",
            message = "Go to the site to see the new lead",
            from_email= "test@test.com",
            recipient_list=["test2@test.com"]
        )
        return super(LeadCreateView,self).form_valid(form)
    
class LeadUpdateView(OrganisorAndLoginRequiredMixin, UpdateView):
    template_name = "leads/lead_update.html"
    form_class = LeadModelForm

    def get_queryset(self):
        user = self.request.user
        return Lead.objects.filter(organisation = user.userprofile)
    
    def get_success_url(self):
        return reverse("leads:lead-list")

class LeadDeleteView(OrganisorAndLoginRequiredMixin, DeleteView):
    template_name = "leads/lead_delete.html"

    def get_queryset(self):
        user = self.request.user
        return Lead.objects.filter(organisation = user.userprofile)
    
    def get_success_url(self):
        return reverse("leads:lead-list")

class SignupView(CreateView):
    template_name = "registration/signup.html"
    form_class = CustomedUserCreationForm

    def get_success_url(self):
        return reverse("login")

class CategoryListView(OrganisorAndLoginRequiredMixin, ListView):
    template_name = "leads/category_list.html"
    context_object_name = "category_list"

    def get_context_data(self, **kwargs):
        context = super(CategoryListView, self).get_context_data(**kwargs)
        user = self.request.user

        if user.is_organisor:
            queryset = Lead.objects.filter(organisation = user.userprofile)
        else:
            queryset = Lead.objects.filter(organisation = user.agent.organisation)

        context.update(
            {
                "unassigned_lead_count":Lead.objects.filter(category__isnull = True).count()
            }
        )
        return context
    
    def get_queryset(self):
        user = self.request.user
        #initial query set of leads for tiktok
        if user.is_organisor:
            queryset = Category.objects.filter(organisation = user.userprofile)
        else:
            queryset = Category.objects.filter(organisation = user.agent.organisation)
        return queryset

class CategoryDetailView(LoginRequiredMixin, DetailView):
    template_name = "leads/category_detail.html"
    context_object_name = "category"
    
    def get_queryset(self):
        user = self.request.user
        #initial query set of leads for tiktok
        if user.is_organisor:
            queryset = Category.objects.filter(organisation = user.userprofile)
        else:
            queryset = Category.objects.filter(organisation = user.agent.organisation)
        return queryset

class LeadCategoryUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "leads/lead_category_update.html"
    form_class = LeadCategoryUpdateForm
    
    def get_queryset(self):
        user = self.request.user
        if user.is_organisor:
            queryset = Lead.objects.filter(organisation = user.userprofile)
        else:
            queryset = Lead.objects.filter(organisation = user.agent.organisation)
            #filter by sales person
            queryset = queryset.filter(agent__user = user)
        return queryset
    
    def get_success_url(self):
        return reverse("leads:lead-detail", kwargs={"pk": self.get_object().id})

class AssignAgentView(OrganisorAndLoginRequiredMixin, FormView):
    template_name = "leads/assign_agent.html"
    form_class = AssignAgentForm

    def get_form_kwargs(self, **kwargs):
        kwargs = super(AssignAgentView, self).get_form_kwargs(**kwargs)
        kwargs.update ({
            "request": self.request
        })
        return kwargs
    
    def get_success_url(self):
        return reverse("leads:lead-list")
    
    def form_valid(self, form):
        agent = form.cleaned_data["agent"]
        lead = Lead.objects.get(id = self.kwargs["pk"])
        lead.agent = agent
        lead.save()
        return super(AssignAgentView, self).form_valid(form)
    
class PurchaseProductView(OrganisorAndLoginRequiredMixin, FormView):
    template_name = "leads/purchase_product.html"
    form_class = PurchaseProductForm

    def get_form_kwargs(self, **kwargs):
        kwargs = super(AssignAgentView, self).get_form_kwargs(**kwargs)
        kwargs.update ({
            "request": self.request
        })
        return kwargs
    
    def get_success_url(self):
        return reverse("leads:lead-list")
    
    def form_valid(self, form):
        agent = form.cleaned_data["agent"]
        lead = Lead.objects.get(id = self.kwargs["pk"])
        lead.agent = agent
        lead.save()
        return super(AssignAgentView, self).form_valid(form)

def lead_list(request):
    leads = Lead.objects.all()
    context = {
        "leads" : leads
    }
    return render(request, "leads/lead_list.html", context)

def landing_page(request):
    return render(request, "landing.html")

def lead_detail(request, pk):
    lead = Lead.objects.get(id = pk)
    context = {
        "lead" : lead
    }
    return render(request, "leads/lead_detail.html", context)

def lead_create(request):
    form = LeadModelForm()
    if request.method == "POST":
        form  = LeadModelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/leads')
    context = {
        "form": form
    }
    return render(request, "leads/lead_create.html",context)

def lead_update(request, pk):
    lead = Lead.objects.get(id = pk)
    form = LeadModelForm(instance = lead)
    if request.method == "POST":
        form  = LeadModelForm(request.POST, instance= lead)
        if form.is_valid():
            form.save()
            return redirect('/leads')
    context = {
        "form": form,
        'lead':lead
    }
    return render(request, "leads/lead_update.html", context)

def lead_delete(request, pk):
    lead = Lead.objects.get(id = pk)
    lead.delete()
    return redirect('/leads')

