from typing import Any, List, Optional

from fastapi import Depends, UploadFile, File
from pydantic import Field


from app.utils import AppModel

from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data

from ..service import Service, get_service

from . import router


@router.post("/file")
def upload_file(
    id: str,file: UploadFile, svc: Service = Depends(get_service), jwt_data: JWTData = Depends(parse_jwt_user_data)
):
    """
    file.filename: str - Название файла
    file.file: BytesIO - Содержимое файла
    """
    url = svc.s3_service.upload_file(file.file, file.filename)
    svc.repository.update_pic(id, jwt_data.user_id, url)
    return {"msg": url}

@router.post("/files")
def upload_files(
    id: str,files: List[UploadFile], svc: Service = Depends(get_service), jwt_data: JWTData = Depends(parse_jwt_user_data)
):
    """
    file.filename: str - Название файла
    file.file: BytesIO - Содержимое файла
    """
    
    result = []
    for file in files:
        url = svc.s3_service.upload_file(file.file, file.filename)
        result.append(url)
    svc.repository.update_pic(id, jwt_data.user_id, url)
    return {"msg": files}