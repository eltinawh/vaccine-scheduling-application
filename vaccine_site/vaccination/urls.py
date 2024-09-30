from django.urls import path
from vaccination import views


app_name = "vaccination"

urlpatterns = [
    path("", views.VaccinationListView.as_view(), name="vaccination-list"),
    path("<int:pk>/", views.VaccinationDetailView.as_view(), name="vaccination-detail"),
    path("choose-vaccine/", views.ChooseVaccineView.as_view(), name="choose-vaccine"),
    path("choose-campaign/<int:vaccine_id>/", views.ChooseCampaignView.as_view(), name="choose-campaign"),
    path("choose-slot/<int:campaign_id>/", views.ChooseSlotView.as_view(), name="choose-slot"),
    path("confirm-vaccination/<int:campaign_id>/<int:slot_id>/", views.ConfirmVaccinationView.as_view(), name="confirm-vaccination"),
    path("appointment-letter/<int:vaccination_id>/", views.appointment_letter, name="appointment-letter"),
    path("vaccination-certificate/<int:vaccination_id>/", views.vaccination_certificate, name="vaccination-certificate"),
    path("approve-vaccination/<int:vaccination_id>/", views.approve_vaccination, name="approve-vaccination"),
]