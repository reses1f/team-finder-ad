from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from projects.forms import ProjectForm
from projects.models import Project

PAGE_SIZE = 12


def project_list_view(request):
    queryset = Project.objects.select_related("owner").prefetch_related("participants")
    paginator = Paginator(queryset, PAGE_SIZE)
    page = paginator.get_page(request.GET.get("page"))
    return render(request, "projects/project_list.html", {"projects": page})


@login_required
def favorite_projects_view(request):
    queryset = request.user.favorites.select_related("owner").prefetch_related(
        "participants"
    )
    paginator = Paginator(queryset, PAGE_SIZE)
    page = paginator.get_page(request.GET.get("page"))
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
    if request.method == "POST" and form.is_valid():
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
    if request.method == "POST" and form.is_valid():
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
    if favorites.filter(pk=project.pk).exists():
        favorites.remove(project)
        favorited = False
    else:
        favorites.add(project)
        favorited = True
    return JsonResponse({"status": "ok", "favorited": favorited})


@login_required
@require_POST
def complete_project_view(request, project_id):
    project = get_object_or_404(Project, pk=project_id, owner=request.user)
    if project.status != Project.STATUS_OPEN:
        return JsonResponse({"status": "error"}, status=400)
    project.status = Project.STATUS_CLOSED
    project.save(update_fields=["status"])
    return JsonResponse({"status": "ok", "project_status": "closed"})


@login_required
@require_POST
def toggle_participate_view(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if project.owner_id == request.user.pk:
        return JsonResponse({"status": "error"}, status=400)
    participants = project.participants
    if participants.filter(pk=request.user.pk).exists():
        participants.remove(request.user)
        is_participant = False
    else:
        participants.add(request.user)
        is_participant = True
    return JsonResponse({"status": "ok", "participant": is_participant})
