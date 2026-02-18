"""User management API (admin-only create, list, update role)."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.audit import log_audit
from app.core.auth import require_roles
from app.core.password import hash_password
from app.db.session import get_db
from app.models import User
from app.schemas.user import UserCreate, UserResponse, UserRoleUpdate

router = APIRouter(prefix="/users", tags=["users"])


@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(
    body: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["admin"])),
) -> UserResponse:
    """Create a user (admin only). Returns 409 if email already exists."""
    existing = (
        db.execute(select(User).where(User.email == body.email.strip().lower()))
        .scalars()
        .first()
    )
    if existing is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A user with this email already exists",
        )
    user = User(
        email=body.email.strip().lower(),
        password_hash=hash_password(body.password),
        role=body.role,
    )
    db.add(user)
    db.flush()
    log_audit(
        db,
        action="CREATE",
        entity_type="User",
        entity_id=user.id,
        user_id=current_user.id,
        summary="user created",
    )
    db.commit()
    db.refresh(user)
    return UserResponse.model_validate(user)


@router.get("", response_model=list[UserResponse])
def list_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["admin"])),
) -> list[UserResponse]:
    """List all users (admin only). Response excludes password/password_hash."""
    users = db.execute(select(User).order_by(User.id.asc())).scalars().all()
    return [UserResponse.model_validate(u) for u in users]


@router.patch("/{user_id:int}/role", response_model=UserResponse)
def update_user_role(
    user_id: int,
    body: UserRoleUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["admin"])),
) -> UserResponse:
    """Update a user's role (admin only). Returns 404 if user not found."""
    user = db.get(User, user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    user.role = body.role
    log_audit(
        db,
        action="UPDATE",
        entity_type="User",
        entity_id=user_id,
        user_id=current_user.id,
        summary=f"role changed to {body.role}",
    )
    db.commit()
    db.refresh(user)
    return UserResponse.model_validate(user)
