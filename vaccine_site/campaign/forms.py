from typing import Any, Mapping
from django.core.files.base import File
from django.db.models.base import Model
from django.forms import ModelForm
from django.forms.utils import ErrorList
from campaign.models import Campaign, Slot
from center.models import Storage
from django import forms


class CampaignForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(CampaignForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"
    class Meta:
        model = Campaign
        fields = "__all__"
        
        
class SlotForm(ModelForm):
    def __init__(self, campaign_id, *args, **kwargs):
        super(SlotForm, self).__init__(*args, **kwargs)
        self.fields["campaign"].queryset = Campaign.objects.filter(id=campaign_id)
        self.fields["campaign"].disabled = True
        self.fields["reserved"].disabled = True
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"
    
    class Meta:
        model = Slot
        fields = "__all__"
    
    def clean(self):
        cleaned_data = super().clean()
        campaign = cleaned_data.get('campaign')
        date = cleaned_data.get('date')
        
        if campaign:
            center = campaign.center
            vaccine = campaign.vaccine
            
            # Check if the corresponding Storage instance exists
            if not Storage.objects.filter(center=center, vaccine=vaccine).exists():
                self.add_error(
                    None,  # Add as a non-field error
                    "No storage found for this center and vaccine combination. Create the storage first!"
                )
                
            if date:
                if not (campaign.start_date <= date <= campaign.end_date):
                    self.add_error(
                        'date',
                        f'The slot date must be between {campaign.start_date} and {campaign.end_date}.'
                    )
        
        return cleaned_data