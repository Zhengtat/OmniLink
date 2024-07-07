from django.urls import path
from .views import (lead_list, lead_detail, lead_create, lead_update, lead_delete, 
                    LeadDetailView, LeadListView, LeadCreateView, LeadUpdateView, 
                    LeadDeleteView, AssignAgentView, CategoryListView, CategoryDetailView,
                    LeadCategoryUpdateView, TaskCreateView,TaskUpdateView,TaskDeleteView)

app_name = "leads"

urlpatterns = [
    path('', LeadListView.as_view(), name='lead-list'),
    path('create/', LeadCreateView.as_view(), name='lead-create'),
    path('<int:pk>/', LeadDetailView.as_view(), name='lead-detail'),
    path('<int:pk>/update/', LeadUpdateView.as_view(), name='lead-update'),
    path('<int:pk>/delete/', LeadDeleteView.as_view(), name='lead-delete'),
    path('<int:pk>/assign-agent/', AssignAgentView.as_view(), name = 'assign-agent'),
    path('categories/', CategoryListView.as_view(), name = 'category-list'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name = 'category-detail'),
    path('<int:pk>/category/', LeadCategoryUpdateView.as_view(), name = 'lead-category-update'),
    path('<int:pk>/task/create/', TaskCreateView.as_view(), name='lead-task-create'),
    path('task/<int:pk>/', TaskUpdateView.as_view(), name='lead-task-update'),
    path('task/<int:pk>/delete/', TaskDeleteView.as_view(), name='lead-task-delete'),
]