from math import ceil

from pydantic import BaseModel


class Pagination(BaseModel):

    page: int

    limit: int

    total_records: int

    total_pages: int


class PaginatedResponse(BaseModel):

    data: list

    pagination: Pagination


def build_pagination(
    page: int,
    limit: int,
    total_records: int
) -> Pagination:

    return Pagination(

        page=page,

        limit=limit,

        total_records=total_records,

        total_pages=ceil(total_records / limit)
        if total_records
        else 1
    )
