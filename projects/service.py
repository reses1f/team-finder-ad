from django.core.paginator import Paginator

from projects.constants import PAGE_SIZE


def get_paginated_page(request, queryset, page_size=PAGE_SIZE):
    paginator = Paginator(queryset, page_size)
    page_number = request.GET.get("page")
    return paginator.get_page(page_number)


def optimize_project_queryset(queryset):
    return queryset.select_related("owner").prefetch_related("participants")


