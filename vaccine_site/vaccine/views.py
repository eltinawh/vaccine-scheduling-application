from django.shortcuts import render, get_object_or_404
from django.views import View
from vaccine.models import Vaccine
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from vaccine.forms import VaccineForm
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator


@method_decorator(login_required, name="dispatch")
class VaccineListView(View):
    def get(self, request):
        vaccine_list = Vaccine.objects.all().order_by("name")
        paginator = Paginator(vaccine_list, 5)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        context = {
            "page_obj": page_obj
        }
        return render(request, "vaccine-list.html", context)
    

@method_decorator(login_required, name="dispatch")
class VaccineDetailView(View):
    def get(self, request, id):
        try:
            vaccine = Vaccine.objects.get(id=id)
        except Vaccine.DoesNotExist:
            raise Http404("Vaccine instance not found")
        
        context = {
            "object": vaccine
        }
        return render(request, "vaccine-detail.html", context)
    

@method_decorator(login_required, name="dispatch")  
@method_decorator(permission_required("vaccine.add_vaccine", raise_exception=True), name="dispatch")  
class CreateVaccineView(View):
    form_class = VaccineForm
    template_name = "create-vaccine.html"
    
    def get(self, request):
        context = {
            "form": self.form_class()
        }
        return render(request, self.template_name, context)
    
    
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Vaccine Created Successfully")
            return HttpResponseRedirect(reverse("vaccine:list"))
        messages.error(request, "Please enter valid data")
        return render(request, self.template_name, {"form": form})


@method_decorator(login_required, name="dispatch")  
@method_decorator(permission_required("vaccine.change_vaccine", raise_exception=True), name="dispatch") 
class UpdateVaccineView(View):
    form_class = VaccineForm
    template_name = "update-vaccine.html"
    
    def get(self, request, id):
        vaccine = get_object_or_404(Vaccine, id=id)
        context = {
            "form": self.form_class(instance=vaccine)
        }
        return render(request, self.template_name, context)
    
    def post(self, request, id):
        vaccine = get_object_or_404(Vaccine, id=id)
        form = self.form_class(request.POST, instance=vaccine)
        if form.is_valid():
            form.save()
            messages.success(request, "Vaccine Updated Successfully")
            return HttpResponseRedirect(reverse("vaccine:detail", kwargs={"id": vaccine.id}))
        messages.error(request, "Please enter valid data")
        return render(request, self.template_name, {"form": form})
    

@method_decorator(login_required, name="dispatch")  
@method_decorator(permission_required("vaccine.delete_vaccine", raise_exception=True), name="dispatch")     
class DeleteVaccineView(View):
    template_name = "delete-vaccine.html"
    
    def get(self, request, id):
        vaccine = get_object_or_404(Vaccine, id=id)
        context = {
            "vaccine": vaccine
        }
        return render(request, self.template_name, context)
    
    def post(self, request, id):
        vaccine = get_object_or_404(Vaccine, id=id)
        vaccine.delete()
        messages.success(request, "Vaccine Deleted Successfully")
        return HttpResponseRedirect(reverse("vaccine:list"))
