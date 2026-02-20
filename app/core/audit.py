"""Audit logging helper: persist CREATE/UPDATE/DELETE for core entities."""

from sqlalchemy.orm import Session

from app.models import AuditLog


def log_audit(
    db: Session,
    action: str,
    entity_type: str,
    entity_id: int,
    tenant_id: int,
    user_id: int | None = None,
    summary: str | None = None,
) -> None:
    """Append an audit log entry; commit is left to the caller. tenant_id is required (use current_user.tenant_id)."""
    entry = AuditLog(
        action=action,
        entity_type=entity_type,
        entity_id=entity_id,
        tenant_id=tenant_id,
        user_id=user_id,
        summary=summary,
    )
    db.add(entry)
