from django.urls import path
from campaign import views

app_name = "campaign"

urlpatterns = [
    path("", views.CampaignListView.as_view(), name="campaign-list"),
    path("<int:pk>/", views.CampaignDetailView.as_view(), name="campaign-detail"),
    path("create/", views.CreateCampaignView.as_view(), name="create-campaign"),
    path("update/<int:pk>", views.UpdateCampaignView.as_view(), name="update-campaign"),
    path("delete/<int:pk>",views.DeleteCampaignView.as_view(), name="delete-campaign"),
]