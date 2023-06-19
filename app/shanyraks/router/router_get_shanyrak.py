from typing import Any, List, Optional

from fastapi import Depends, Response
from pydantic import Field

from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data
from app.utils import AppModel

from ..service import Service, get_service
from . import router


class GetShanyrakResponse(AppModel):
    id: Any = Field(alias="_id")
    type: str
    price: int
    address: str
    area: float
    rooms_count: int
    description: str
    user_id: Any
    location: Any
    media: List[str] = []


# class GetShanyraksResponse (AppModel):
#     total: int
#     objects: List[GetShanyrakResponse]


@router.get("/all", response_model=List[GetShanyrakResponse])
def get_all_shanyraks(
        jwt_data: JWTData = Depends(parse_jwt_user_data),
        svc: Service = Depends(get_service)
) -> List[GetShanyrakResponse]:
    shanyraks = svc.repository.get_all_shanyraks(user_id=jwt_data.user_id)
    # return Response(status_code=200)
    return [GetShanyrakResponse(**shanyrak) for shanyrak in shanyraks]


@router.get("/{shanyrak_id:str}", response_model=GetShanyrakResponse)
def get_shanyrak(
        shanyrak_id: str,
        jwt_data: JWTData = Depends(parse_jwt_user_data),
        svc: Service = Depends(get_service),
) -> dict[str, str]:
    shanyrak = svc.repository.get_shanyrak_by_id(shanyrak_id=shanyrak_id, user_id=jwt_data.user_id)
    if not shanyrak:
        return Response(status_code=404)
    return GetShanyrakResponse(**shanyrak)


@router.get("/")
def get_shanyraks(
    limit: int,
    offset: int,
    rooms_count: Optional[int] = None,
    price_from: Optional[int] = None,
    price_until: Optional[int] = None,
    latitude: Optional[float] = None,
    longitude: Optional[float] = None,
    radius: Optional[float] = None,
    svc: Service = Depends(get_service),
):
    paginated = svc.repository.pagination_shanyraks(limit, offset, rooms_count, price_from, price_until, latitude, longitude, radius)
    return {"total": len(paginated), "objects": paginated}
