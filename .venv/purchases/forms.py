from django import forms
from leads.models import Lead, Agent, Product, Purchase
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.contrib.auth import get_user_model

class CreatePurchaseForm(forms.ModelForm):
    product = forms.ModelChoiceField(queryset=Product.objects.all())
    lead = forms.ModelChoiceField(queryset= Lead.objects.none())

    def __init__(self, *args, **kwargs):
        #request is agent
        request = kwargs.pop("request")
        user = request.user
        if user.is_organisor:
            leads = Lead.objects.filter(organisation = user.userprofile, agent__isnull = False)
        else:
            leads = Lead.objects.filter(organisation = user.agent.organisation, agent__isnull = False)
            leads = leads.filter(agent__user = user)
        super(CreatePurchaseForm,self).__init__(*args, **kwargs)
        self.fields["lead"].queryset = leads
    
    class Meta:
        model = Purchase
        fields = (
            'payment_method',
            'quantity',
        )