from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from notes_sync.database import models
from notes_sync import schemas
from notes_sync.database.connection import get_db
from notes_sync.dependencies import oauth2


api_router = APIRouter(prefix="/config", tags=["Account"])


@api_router.get(
    "",
    responses={
        schemas.ConfigGetResponse.status_code(): {"model": schemas.ConfigGetResponse},
    },
    dependencies=[Depends(oauth2)],
)
async def get_config(
    user: models.User = Depends(oauth2), db: Session = Depends(get_db)
) -> schemas.ConfigGetResponse:
    return schemas.ConfigGetResponse(config=user.get_config())


@api_router.put(
    "",
    responses={
        schemas.EmptyOkResponse.status_code(): {"model": schemas.EmptyOkResponse}
    },
    dependencies=[Depends(oauth2)],
)
async def put_config(
    request: schemas.ConfigPutRequest,
    user: models.User = Depends(oauth2),
    db: Session = Depends(get_db),
) -> schemas.EmptyOkResponse:
    has_update = user.update_config(request.config)
    if has_update:
        db.add(user)
        db.commit()
    return schemas.EmptyOkResponse()
