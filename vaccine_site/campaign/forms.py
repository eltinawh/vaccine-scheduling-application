from typing import Any, Mapping
from django.core.files.base import File
from django.db.models.base import Model
from django.forms import ModelForm
from django.forms.utils import ErrorList
from campaign.models import Campaign, Slot


class CampaignForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(CampaignForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"
    class Meta:
        model = Campaign
        fields = "__all__"
        
        
class SlotForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(SlotForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"
    class Meta:
        model = Slot
        fields = "__all__"