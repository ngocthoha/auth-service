from typing import Any, List
from fastapi import APIRouter, Body, Depends, HTTPException, status, Response
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.api.deps import get_current_active_user, check_permission, get_db
from app.models.user import User
from app.schemas.user import User as UserSchema, UserCreate, UserUpdate
from app.services.auth_service import ResourceEnum, ActionEnum
from app.services.user_service import UserService

router = APIRouter()


@router.get("/me", response_model=UserSchema)
def read_user_me(
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Get current user
    """
    return current_user


@router.put("/me", response_model=UserSchema)
def update_user_me(
    user_in: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Update current user
    """
    # Prevent users from changing their own role
    if user_in.role is not None and user_in.role != current_user.role:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot change own role",
        )
    
    user = UserService.update(db, db_user=current_user, user_in=user_in)
    return user


@router.get("", response_model=List[UserSchema])
def read_users(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(check_permission(ResourceEnum.USERS, ActionEnum.LIST)),
) -> Any:
    """
    Retrieve users - requires LIST permission
    """
    users = db.query(User).offset(skip).limit(limit).all()
    return users


@router.post("", response_model=UserSchema, status_code=status.HTTP_201_CREATED)
def create_user(
    user_in: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(check_permission(ResourceEnum.USERS, ActionEnum.CREATE)),
) -> Any:
    """
    Create a new user - requires CREATE permission
    """
    # Check if user with this email already exists
    user = UserService.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The user with this email already exists",
        )
    
    return UserService.create(db, user_in=user_in)


@router.get("/{user_id}", response_model=UserSchema)
def read_user_by_id(
    user_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(check_permission(ResourceEnum.USERS, ActionEnum.READ)),
) -> Any:
    """
    Get a specific user by id - requires READ permission
    """
    user = UserService.get_by_id(db, user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return user


@router.put("/{user_id}", response_model=UserSchema)
def update_user(
    user_id: str,
    user_in: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(check_permission(ResourceEnum.USERS, ActionEnum.UPDATE)),
) -> Any:
    """
    Update a user - requires UPDATE permission
    """
    user = UserService.get_by_id(db, user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    
    user = UserService.update(db, db_user=user, user_in=user_in)
    return user


@router.delete("/{user_id}")
def delete_user(
    user_id: str,
    response: Response,
    db: Session = Depends(get_db),
    current_user: User = Depends(check_permission(ResourceEnum.USERS, ActionEnum.DELETE)),
):
    """
    Delete a user - requires DELETE permission
    """
    user = UserService.get_by_id(db, user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    
    if user.id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete yourself",
        )
    
    db.delete(user)
    db.commit()
    
    response.status_code = status.HTTP_204_NO_CONTENT 