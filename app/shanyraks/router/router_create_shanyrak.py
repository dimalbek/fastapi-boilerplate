from typing import Any, Optional, List

from fastapi import Depends, Response
from pydantic import Field


from app.utils import AppModel

from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data

from ..service import Service, get_service

from . import router


# class Coordinates(AppModel):
#     longitude: float
#     latitude: float


class CreateShanyrakRequest(AppModel):
    type: str
    price: int
    address: str
    area: float
    rooms_count: int
    description: str
    # location: Optional[Coordinates]


class CreateShanyrakResponse(AppModel):
    id: Any = Field(alias="_id")


@router.post("/", response_model=CreateShanyrakResponse)
def create_shanyrak(
    input: CreateShanyrakRequest,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
) -> dict[str, str]:
    # save_data = input.dict() | svc.here_service.get_coordinates(input.address)
    # print(save_data)
    dict = input.dict()
    location = svc.here_service.get_coordinates(input.address)
    dict.update(location)
    print(dict)
    shanyrak_id = svc.repository.create_shanyrak(user_id=jwt_data.user_id, payload=dict)
    return CreateShanyrakResponse(id=shanyrak_id)



# @router.get("/location/", response_model=CreateShanyrakResponse)
# def create_shanyrak(
#     input: CreateShanyrakRequest,
#     jwt_data: JWTData = Depends(parse_jwt_user_data),
#     svc: Service = Depends(get_service),
# ) -> dict[str, str]:
#     shanyrak = svc.repository.get_shanyrak_by_id(shanyrak_id=shanyrak_id, user_id=jwt_data.user_id)
#     if not shanyrak:
#         return Response(status_code=404)
#     location = svc.here_service.get_coordinates(shanyrak['address'])
#     shanyrak['location'] = location
#     return CreateShanyrakRequest(id = shanyrak_id)
