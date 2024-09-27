from django.urls import path
from campaign import views

app_name = "campaign"

urlpatterns = [
    path("", views.CampaignListView.as_view(), name="campaign-list"),
    path("<int:pk>/", views.CampaignDetailView.as_view(), name="campaign-detail"),
    path("create/", views.CreateCampaignView.as_view(), name="create-campaign"),
    path("update/<int:pk>", views.UpdateCampaignView.as_view(), name="update-campaign"),
    path("delete/<int:pk>",views.DeleteCampaignView.as_view(), name="delete-campaign"),
    path("<int:campaign_id>/slot/",views.SlotListView.as_view(), name="slot-list"),
    path("slot/<int:pk>", views.SlotDetailView.as_view(), name="slot-detail"),
    path("<int:campaign_id>/slot/create/", views.CreateSlotView.as_view(), name="create-slot"),
    path("slot/update/<int:pk>/", views.UpdateSlotView.as_view(), name="update-slot"),
    path("slot/delete/<int:pk>/", views.DeleteSlotView.as_view(), name="delete-slot"),
]