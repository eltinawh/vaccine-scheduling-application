from django import forms
from django.contrib import admin
from campaign.models import Campaign, Slot

# Custom form for Slot model validation
class SlotInlineForm(forms.ModelForm):
    class Meta:
        model = Slot
        fields = "__all__"
        
    def clean(self):
        cleaned_data = super().clean()
        campaign = cleaned_data.get('campaign')
        date = cleaned_data.get('date')
        
        if campaign and date:
            if not (campaign.start_date <= date <= campaign.end_date):
                self.add_error("date", f"The slot must be between {campaign.start_date} and {campaign.end_date}")
                
        return cleaned_data
    

# Slot inline with custom form
class SlotInline(admin.TabularInline):
    model = Slot
    form = SlotInlineForm # Apply custom form validation
    readonly_fields = ["reserved"]
    
    
# Campaign admin with Slot inline
class CustomCampaignAdmin(admin.ModelAdmin):
    inlines = [SlotInline]
    search_fields = ["vaccine__name", "center__name"]
    list_display = ["vaccine","center","start_date","end_date"]
    ordering = ["start_date"]
    fields = (
        ("vaccine"),
        ("center"),
        ("start_date","end_date"),
        ("agents"),
    )
    

admin.site.register(Campaign, CustomCampaignAdmin)