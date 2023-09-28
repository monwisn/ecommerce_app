from typing import List

from django.core.paginator import Paginator
from django.db.models.query import QuerySet
from django.http import HttpRequest


def paginate_queryset(request: HttpRequest, queryset: QuerySet, num_items: int) -> List[QuerySet]:
    paginator = Paginator(queryset, num_items)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return page_obj
