from django.urls import path
from center import views

app_name = "center"

urlpatterns = [
    path("", views.center_list, name="list"),
    path("<int:id>", views.center_detail, name="detail"),
    path("create/", views.create_center, name="create"),
    path("update/<int:id>", views.update_center, name="update"),
    path("delete/<int:id>",views.delete_center, name="delete"),
    path("<int:center_id>/storage/", views.StorageList.as_view(), name="storage-list"),
    path("storage/<int:pk>/", views.StorageDetail.as_view(), name="storage-detail"),
    path("<int:center_id>/storage/create/", views.CreateStorage.as_view(), name="create-storage"),
    path("storage/update/<int:pk>/", views.UpdateStorage.as_view(), name="update-storage"),
    path("storage/delete/<int:pk>/", views.DeleteStorage.as_view(), name="delete-storage"),
]