from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from .constants import PAGE_SIZE 
from projects.forms import ProjectForm
from projects.models import Project
from .service import get_paginated_page, optimize_project_queryset
from http import HTTPStatus





def project_list_view(request):
    queryset = optimize_project_queryset(Project.objects.all())
    page = get_paginated_page(request, queryset)
    return render(request, "projects/project_list.html", {"projects": page})


@login_required
def favorite_projects_view(request):
    queryset = optimize_project_queryset(request.user.favorites.all())
    page = get_paginated_page(request, queryset)
    return render(request, "projects/favorite_projects.html", {"projects": page})


def project_detail_view(request, project_id):
    project = get_object_or_404(
        Project.objects.select_related("owner").prefetch_related("participants"),
        pk=project_id,
    )
    return render(request, "projects/project-details.html", {"project": project})


@login_required
def project_create_view(request):
    form = ProjectForm(request.POST or None)
    if form.is_valid():
        project = form.save(commit=False)
        project.owner = request.user
        project.save()
        project.participants.add(request.user)
        return redirect("projects:detail", project_id=project.pk)
    return render(
        request,
        "projects/create-project.html",
        {"form": form, "is_edit": False},
    )


@login_required
def project_edit_view(request, project_id):
    project = get_object_or_404(Project, pk=project_id, owner=request.user)
    form = ProjectForm(request.POST or None, instance=project)
    if form.is_valid():
        form.save()
        return redirect("projects:detail", project_id=project.pk)
    return render(
        request,
        "projects/create-project.html",
        {"form": form, "is_edit": True},
    )


@login_required
@require_POST
def toggle_favorite_view(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    favorites = request.user.favorites
    
    if is_favorite := favorites.filter(pk=project.pk).exists():
        favorites.remove(project)
    else:
        favorites.add(project)
        
    return JsonResponse({"status": "ok", "favorited": not is_favorite})


@login_required
@require_POST
def complete_project_view(request, project_id):
    project = get_object_or_404(Project, pk=project_id, owner=request.user)
    if project.status != Project.STATUS_OPEN:
        return JsonResponse({"status": "error"}, status=HTTPStatus.BAD_REQUEST)

    project.status = Project.STATUS_CLOSED
    project.save(update_fields=["status"])
    return JsonResponse({"status": "ok", "project_status": "closed"})


@login_required
@require_POST
@login_required
@require_POST
def toggle_participate_view(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if project.owner_id == request.user.pk:
        return JsonResponse({"status": "error"}, status=HTTPStatus.BAD_REQUEST)
        
    participants = project.participants
    if is_participant := participants.filter(pk=request.user.pk).exists():
        participants.remove(request.user)
    else:
        participants.add(request.user)
        
    return JsonResponse({"status": "ok", "participant": not is_participant})

