from django import forms
from .models import Lead, Agent, Product, Task
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.contrib.auth import get_user_model

User = get_user_model()

class LeadModelForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = (
            'first_name',
            'last_name',
            'contact_info',
            'age',
            'agent',
            'description',
            'email',
        )

class TaskModelForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = (
            'notes',
            'status',
            'due_date'
        )

class LeadForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    age = forms.IntegerField(min_value=0)

class CustomedUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username',)
        field_classes = {'username' : UsernameField}

class AssignAgentForm(forms.Form):
    agent = forms.ModelChoiceField(queryset=Agent.objects.none())

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request')
        agents = Agent.objects.filter(organisation = request.user.userprofile)
        super(AssignAgentForm, self).__init__(*args, **kwargs)
        self.fields["agent"].queryset = agents

class LeadCategoryUpdateForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = (
            'category',
        )
