from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from .constants import PAGE_SIZE
from .service import get_paginated_page
from users.forms import (
    CustomPasswordChangeForm,
    LoginForm,
    ProfileEditForm,
    RegistrationForm,
)
from users.models import User


FILTER_HANDLERS = {
    "owners-of-favorite-projects": lambda user: User.objects.filter(
        owned_projects__in=user.favorites.all()
    ),
    "owners-of-participating-projects": lambda user: User.objects.filter(
        owned_projects__in=user.participated_projects.all()
    ),
    "interested-in-my-projects": lambda user: User.objects.filter(
        favorites__in=user.owned_projects.all()
    ),
    "participants-of-my-projects": lambda user: User.objects.filter(
        participated_projects__owner=user,
    ).exclude(pk=user.pk),
}


def register_view(request):
    if request.user.is_authenticated:
        return redirect("projects:list")
    form = RegistrationForm(request.POST or None)
    if form.is_valid():

        user = form.save()
        login(request, user)
        return redirect("projects:list")
    return render(request, "users/register.html", {"form": form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect("projects:list")
    form = LoginForm(request.POST or None)
    if form.is_valid():

        login(request, form.user)
        return redirect("projects:list")
    return render(request, "users/login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("projects:list")


def user_detail_view(request, user_id):
    profile_user = get_object_or_404(
        User.objects.prefetch_related("owned_projects"),
        pk=user_id,
    )
    return render(request, "users/user-details.html", {"user": profile_user})


def participants_list_view(request):
    queryset = User.objects.all().order_by("-id")
    active_filter = None
    if request.user.is_authenticated:
        active_filter = request.GET.get("filter")
        handler = FILTER_HANDLERS.get(active_filter)
        if handler:
            queryset = handler(request.user).distinct().order_by("-id")
            

    page = get_paginated_page(request, queryset) 


    query_params = request.GET.copy()
    query_params.pop("page", None)
    return render(
        request,
        "users/participants.html",
        {
            "participants": page,
            "active_filter": active_filter,
            "query_string": query_params.urlencode(),
        },
    )


@login_required
def edit_profile_view(request):
    form = ProfileEditForm(
        request.POST or None,
        request.FILES or None,
        instance=request.user,
    )
    if form.is_valid():

        form.save()
        return redirect("users:detail", user_id=request.user.pk)
    return render(request, "users/edit_profile.html", {"form": form})


@login_required
def change_password_view(request):
    form = CustomPasswordChangeForm(request.user, request.POST or None)
    if form.is_valid():

        form.save()
        return redirect("users:detail", user_id=request.user.pk)
    return render(request, "users/change_password.html", {"form": form})
def root_redirect(request):
    return redirect("projects:list")
def root_redirect(request):
    from django.shortcuts import redirect
    return redirect("projects:list")


