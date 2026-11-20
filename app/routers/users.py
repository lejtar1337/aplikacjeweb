from fastapi import APIRouter, HTTPException

from app.dependencies import StorageDep
from app.schemas import UserOut

router = APIRouter(prefix="/users", tags=["users"])


@router.get("", response_model=list[UserOut])
def list_users(storage: StorageDep):
    return list(storage.users.values())


@router.get("/{user_id}", response_model=UserOut)
def get_user(user_id: int, storage: StorageDep):
    user = storage.users.get(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail=f"Użytkownik {user_id} nie istnieje")
    return user
