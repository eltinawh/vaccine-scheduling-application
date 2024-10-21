from django.db import models
from vaccine.models import Vaccine
from center.models import Center, Storage
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError


User = get_user_model()

# Create your models here.
class Campaign(models.Model):
    center = models.ForeignKey(Center, on_delete=models.CASCADE)
    vaccine = models.ForeignKey(Vaccine, on_delete=models.CASCADE)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    agents = models.ManyToManyField(User, blank=True)
    
    def __str__(self):
        return str(self.vaccine.name).upper() + " | " + str(self.center.name).upper()
    
    
class Slot(models.Model):
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    date = models.DateField(null=True, blank=True)
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    max_capacity = models.IntegerField(default=0, null=True, blank=True)
    reserved = models.IntegerField(default=0, null=True, blank=True)
    
    def __str__(self):
        return str(self.date) + " | " + str(self.start_time) + " to " + str(self.end_time)
    
    def reserve_vaccine(campaign_id, slot_id):
        from center.models import Storage
        from django.db.models import F
        
        slot = Slot.objects.get(id=slot_id)
        campaign = Campaign.objects.get(id=campaign_id)
        storage = Storage.objects.get(center=campaign.center, vaccine=campaign.vaccine)
        
        if (storage.total_quantity > 0) and (storage.booked_quantity <= storage.total_quantity) and (slot.reserved <= slot.max_capacity):
            slot.reserved = F("reserved") + 1
            storage.booked_quantity = F("booked_quantity") + 1
            slot.save()
            storage.save()
            return True
        return False
    
    # This is to avoid entering invalid data using create method in shell
    def validate_slot_date(self):
        campaign = Campaign.objects.get(id=self.campaign.id)
        if not (campaign.start_date <= self.date <= campaign.end_date):
            raise ValidationError(f"The slot date must be between {campaign.start_date} and {campaign.end_date}.")
        
    # def clean(self):
    #     # Retrieve the related center and vaccine from the campaign
    #     center = self.campaign.center
    #     vaccine = self.campaign.vaccine
        
    #     # Check if the corresponding Storage instance exists
    #     if not Storage.objects.filter(center=center, vaccine=vaccine).exists():
    #         raise ValidationError("No storage found for this center and vaccine combination.")
    
    def save(self, *args, **kwargs):
        # self.clean()
        self.validate_slot_date()
        super().save(*args, **kwargs)
        