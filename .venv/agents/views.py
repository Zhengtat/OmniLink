from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from leads.models import Agent, Lead
from django.urls import reverse
from .forms import AgentModelForm
from .mixins import OrganisorAndLoginRequiredMixin
from django.core.mail import send_mail
import random


# Create your views here.
class AgentListView(OrganisorAndLoginRequiredMixin, generic.ListView):
    template_name = "agents/agent_list.html"

    def get_queryset(self):
        organisation = self.request.user.userprofile
        return Agent.objects.filter(organisation = organisation)

class AgentCreateView(OrganisorAndLoginRequiredMixin, generic.CreateView):
    template_name = "agents/agent_create.html"
    form_class = AgentModelForm
    
    def get_success_url(self):
        return reverse("agents:agents")
    
    def form_valid(self,form):
        user =  form.save(commit = False)
        user.is_agent = True
        user.is_organisor = False
        user.set_password(f"{random.randint(0,1000000)}")
        user.save()
        Agent.objects.create(
            user = user,
            organisation = self.request.user.userprofile
        )
        send_mail(
            subject = "You are invited to be an agent",
            message = "You are added as an agent on OmniLink. PLease come login to start working",
            from_email = "admin@test.com",
            recipient_list= [user.email]
        )
        return super(AgentCreateView,self).form_valid(form)

class AgentDetailView(OrganisorAndLoginRequiredMixin, generic.DetailView):
    template_name = 'agents/agent_detail.html'
    context_object_name = "agent"

    def get_queryset(self):
        organisation = self.request.user.userprofile
        return Agent.objects.filter(organisation = organisation)
    
    def get_context_data(self, **kwargs):
        context = super(AgentDetailView, self).get_context_data(**kwargs)
        user = self.request.user
        if user.is_organisor:
            queryset = Lead.objects.filter(organisation = user.userprofile, agent__isnull = False)
        else:
            queryset = Lead.objects.filter(organisation = user.agent.organisation, agent__isnull = False)
            #filter by sales person
            queryset = queryset.filter(agent__user = user)
        context.update({
            "agent_leads": queryset
        })
        return context
        
class AgentUpdateView(OrganisorAndLoginRequiredMixin, generic.UpdateView):
    template_name = "agents/agent_update.html"
    form_class = AgentModelForm
    
    def get_success_url(self):
        return reverse("agents:agents")

    def get_queryset(self):
        organisation = self.request.user.userprofile
        return Agent.objects.filter(organisation = organisation)
    
class AgentDeleteView(OrganisorAndLoginRequiredMixin, generic.DeleteView):
    template_name = 'agents/agent_delete.html'
    context_object_name = "agent"

    def get_queryset(self):
        organisation = self.request.user.userprofile
        return Agent.objects.filter(organisation = organisation)
        
    def get_success_url(self):
        return reverse("agents:agents")