from django.shortcuts import render, redirect
from center.models import Center
from center.forms import CenterForm
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse

def center_list(request):
    objects = Center.objects.all()
    context = {
        "center": objects,
    }
    return render(request, "center-list.html", context)

def center_detail(request, id):
    center = Center.objects.get(id=id)
    context = {
        'center': center
    }
    return render(request, "center-detail.html", context)

def create_center(request):
    if request.method == "POST":
        form = CenterForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("center:list"))
        return render(request, "create-center.html", {"form": form})
    # GET
    context = {
        "form": CenterForm()
    }
    return render(request, "create-center.html", context)

def update_center(request, id):
    try:
        center = Center.objects.get(id=id)
    except Center.DoesNotExist:
        raise Http404("Center instance is not found")
    
    if request.method == "POST":
        form = CenterForm(request.POST, instance=center)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("center:detail", kwargs={"id": center.id}))
        return render(request, "update-center.html", {"form": form})
    # GET
    context = {
        "form": CenterForm(instance=center)
    }
    return render(request, "update-center.html", context)

def delete_center(request, id):
    try:
        center = Center.objects.get(id=id)
    except Center.DoesNotExist:
        raise Http404("Center instance is not found")
    
    if request.method == "POST":
        center.delete()
        return HttpResponseRedirect(reverse("center:list"))
    # GET
    context = {
        "center": center,
    }
    return render(request, "delete-center.html", context)