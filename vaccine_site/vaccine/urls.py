from django.urls import path
from vaccine import views

app_name = "vaccine"

urlpatterns = [
    path("", views.VaccineListView.as_view(), name="list"),
    path("<int:id>", views.VaccineDetailView.as_view(), name="detail"),
    path("create/", views.CreateVaccineView.as_view(), name="create"),
    path("update/<int:id>", views.UpdateVaccineView.as_view(), name="update"),
    path("delete/<int:id>", views.DeleteVaccineView.as_view(), name="delete"),
]