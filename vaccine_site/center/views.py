from typing import Any
from django.shortcuts import render, redirect
from center.models import Center, Storage
from center.forms import CenterForm, StorageForm
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.views import generic
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


@login_required
def center_list(request):
    objects = Center.objects.all().order_by("name")
    paginator = Paginator(objects, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {
        "page_obj": page_obj,
    }
    return render(request, "center/center-list.html", context)


@login_required
def center_detail(request, id):
    center = Center.objects.get(id=id)
    context = {
        'center': center
    }
    return render(request, "center/center-detail.html", context)


@login_required
@permission_required("center.add_center", raise_exception=True)
def create_center(request):
    if request.method == "POST":
        form = CenterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Vaccination Center Created Successfully")
            return HttpResponseRedirect(reverse("center:list"))
        messages.error(request, "Please enter valid data")
        return render(request, "center/create-center.html", {"form": form})
    # GET
    context = {
        "form": CenterForm()
    }
    return render(request, "center/create-center.html", context)


@login_required
@permission_required("center.change_center", raise_exception=True)
def update_center(request, id):
    try:
        center = Center.objects.get(id=id)
    except Center.DoesNotExist:
        raise Http404("Center instance is not found")
    
    if request.method == "POST":
        form = CenterForm(request.POST, instance=center)
        if form.is_valid():
            form.save()
            messages.success(request, "Vaccination Center Updated Successfully")
            return HttpResponseRedirect(reverse("center:detail", kwargs={"id": center.id}))
        messages.error(request, "Please enter valid data")
        return render(request, "center/update-center.html", {"form": form})
    # GET
    context = {
        "form": CenterForm(instance=center)
    }
    return render(request, "center/update-center.html", context)


@login_required
@permission_required("center.delete_center", raise_exception=True)
def delete_center(request, id):
    try:
        center = Center.objects.get(id=id)
    except Center.DoesNotExist:
        raise Http404("Center instance is not found")
    
    if request.method == "POST":
        center.delete()
        messages.success(request, "Vaccination Center Deleted Successfully")
        return HttpResponseRedirect(reverse("center:list"))
    # GET
    context = {
        "center": center,
    }
    return render(request, "center/delete-center.html", context)


class StorageList(LoginRequiredMixin, generic.ListView):
    queryset = Storage.objects.all()
    template_name = "storage/storage-list.html"
    ordering = ["id"]
    paginate_by = 5
    
    def get_queryset(self):
        return super().get_queryset().filter(center_id=self.kwargs["center_id"])
    
    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["center_id"] = self.kwargs["center_id"]
        return context

    
class StorageDetailView(LoginRequiredMixin, generic.DetailView):
    model = Storage
    template_name = "storage/storage-detail.html"
    
    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["available_quantity"] = self.object.total_quantity - self.object.booked_quantity
        return context
    

class CreateStorageView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, generic.CreateView):
    model = Storage
    form_class = StorageForm
    template_name = "storage/create-storage.html"
    success_message = "Storage Created Successfully"
    permission_required = ("center.add_storage",)
    
    def get_form_kwargs(self) -> dict[str, Any]:
        kwargs = super().get_form_kwargs()
        kwargs["center_id"] = self.kwargs["center_id"]
        return kwargs
    
    def get_initial(self) -> dict[str, Any]:
        initials = super().get_initial()
        initials["center"] = Center.objects.get(id=self.kwargs["center_id"])
        return initials
    
    def get_success_url(self) -> str:
        return reverse("center:storage-list", kwargs={"center_id": self.kwargs["center_id"]})
    

class UpdateStorageView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, generic.UpdateView):
    model = Storage
    form_class = StorageForm
    template_name = "storage/update-storage.html"
    success_message = "Storage Updated Successfully"
    permission_required = ("center.change_storage",)
    
    def get_form_kwargs(self) -> dict[str, Any]:
        kwargs = super().get_form_kwargs()
        kwargs["center_id"] = self.get_object().center.id
        return kwargs
    
    def get_success_url(self) -> str:
        return reverse("center:storage-list", kwargs={"center_id": self.get_object().center.id})


class DeleteStorageView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, generic.DeleteView):
    model = Storage
    template_name = "storage/delete-storage.html"
    success_message = "Storage Deleted Successfully"
    permission_required = ("center.delete_storage",)
    
    def get_success_url(self):
        return reverse("center:storage-list", kwargs={"center_id": self.get_object().center.id})