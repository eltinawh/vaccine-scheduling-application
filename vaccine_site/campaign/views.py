from django.shortcuts import render
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from campaign.models import Campaign, Slot
from vaccination.models import Vaccination
from campaign.forms import CampaignForm, SlotForm
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy


class CampaignListView(LoginRequiredMixin, generic.ListView):
    model = Campaign
    template_name = "campaign/campaign-list.html"
    paginate_by = 10
    ordering = ["-id"]
    queryset = Campaign.objects.all()
    
    
class CampaignDetailView(LoginRequiredMixin, generic.DetailView):
    model = Campaign
    template_name = "campaign/campaign-detail.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["registrations"] = Vaccination.objects.filter(campaign=self.kwargs["pk"]).count()
        context["campaign_id"] = 1
        return context
    
    
class CreateCampaignView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, generic.CreateView):
    model = Campaign
    form_class = CampaignForm
    permission_required = ("campaign.add_campaign",)
    template_name = "campaign/create-campaign.html"
    success_message = "Campaign Created Successfully"
    success_url = reverse_lazy("campaign:campaign-list")
    

class UpdateCampaignView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, generic.UpdateView):
    model = Campaign
    form_class = CampaignForm
    permission_required = ("campaign.change_campaign",)
    template_name = "campaign/update-campaign.html"
    success_message = "Campaign Updated Successfully"
    success_url = reverse_lazy("campaign:campaign-list")


class DeleteCampaignView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, generic.DeleteView):
    model = Campaign
    permission_required = ("campaign.delete_campaign",)
    template_name = "campaign/delete-campaign.html"
    success_message = "Campaign Deleted Successfully"
    success_url = reverse_lazy("campaign:campaign-list")
    
    
class SlotListView(LoginRequiredMixin, generic.ListView):
    model = Slot
    template_name = "slot/slot-list.html"
    paginate_by = 10
    
    def get_queryset(self):
        queryset = Slot.objects.filter(campaign=self.kwargs["campaign_id"]).order_by("date", "start_time")
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["registrations"] = Vaccination.objects.filter(campaign=self.kwargs["campaign_id"]).count()
        context["campaign_id"] = self.kwargs["campaign_id"]
        return context
    

class SlotDetailView(LoginRequiredMixin, generic.DetailView):
    model = Slot
    template_name = "slot/slot-detail.html"
    
    
class CreateSlotView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, generic.CreateView):
    model = Slot
    form_class = SlotForm
    permission_required = ("campaign.add_slot",)
    template_name = "slot/create-slot.html"
    success_message = "Slot Created Successfully"
    
    def get_success_url(self):
        return reverse_lazy("campaign:slot-list", kwargs={"campaign_id": self.kwargs["campaign_id"]})
    
    def get_initial(self):
        """
        To override the initial value in the form
        """
        initials = super().get_initial()
        initials["campaign"] = Campaign.objects.get(id=self.kwargs["campaign_id"])
        return initials
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["campaign_id"] = self.kwargs["campaign_id"]
        return kwargs
    
    
class UpdateSlotView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, generic.UpdateView):
    model = Slot
    form_class = SlotForm
    permission_required = ("campaign.change_slot",)
    template_name = "slot/update-slot.html"
    success_message = "Slot Updated Successfully"
    
    def get_success_url(self):
        return reverse_lazy("campaign:slot-list", kwargs={"campaign_id": self.get_object().campaign.id})
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["campaign_id"] = self.get_object().campaign.id
        return kwargs


class DeleteSlotView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, generic.DeleteView):
    model = Slot
    permission_required = ("campaign.delete_slot",)
    template_name = "slot/delete-slot.html"
    success_message = "Slot Deleted Successfully"
    
    def get_success_url(self):
        return reverse_lazy("campaign:slot-list", kwargs={"campaign_id": self.get_object().campaign.id})
