from math import ceil
from typing import Generic, TypeVar

from pydantic import BaseModel



T = TypeVar("T")


class PaginationMeta(BaseModel):

    page: int

    limit: int

    total_records: int

    total_pages: int

    has_next: bool

    has_previous: bool


class PaginatedResponse(BaseModel, Generic[T]):

    data: list[T]

    pagination: PaginationMeta


class PaginationParams(BaseModel):

    page: int = 1

    limit: int = 10


def build_pagination_meta(
    page: int,
    limit: int,
    total_records: int,
   
    
) -> PaginationMeta:

    total_pages = ceil(total_records / limit) if total_records else 1

    return PaginationMeta(

        page=page,

        limit=limit,

        total_records=total_records,

        total_pages=total_pages,

        has_next=page < total_pages,

        has_previous=page > 1
    )