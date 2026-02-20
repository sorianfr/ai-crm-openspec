"""Company CRUD routes."""

from datetime import datetime

from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse, Response
from pydantic import ValidationError
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.audit import log_audit
from app.core.csrf import validate_csrf_or_403
from app.core.templates import templates
from app.core.web_auth import get_current_web_user
from app.db.session import get_db
from app.models import Company, User
from app.schemas.company import CompanyFormSchema

router = APIRouter()


def _get_company_or_404(db: Session, company_id: int, tenant_id: int) -> Company | None:
    """Return company if found and belongs to tenant, else None (caller returns 404)."""
    return (
        db.execute(
            select(Company).where(
                Company.id == company_id,
                Company.tenant_id == tenant_id,
            ).limit(1)
        )
        .scalars()
        .first()
    )


@router.get("/companies", response_class=HTMLResponse)
def list_companies(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_web_user),
) -> HTMLResponse:
    companies = (
        db.execute(
            select(Company)
            .where(Company.tenant_id == current_user.tenant_id)
            .order_by(Company.name.asc())
        )
        .scalars()
        .all()
    )
    return templates.TemplateResponse(
        "companies/list.html",
        {"request": request, "companies": companies},
    )


@router.get("/companies/new", response_class=HTMLResponse)
def new_company(
    request: Request,
    current_user: User = Depends(get_current_web_user),
) -> HTMLResponse:
    return templates.TemplateResponse(
        "companies/new.html",
        {"request": request, "errors": []},
    )


@router.post("/companies")
def create_company(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_web_user),
    name: str = Form(""),
    csrf_token: str | None = Form(None),
) -> Response:
    validate_csrf_or_403(request, csrf_token or request.headers.get("X-CSRF-Token"))
    try:
        data = CompanyFormSchema(name=name)
    except ValidationError as e:
        errors = [err["msg"] for err in e.errors()]
        return templates.TemplateResponse(
            "companies/new.html",
            {
                "request": request,
                "errors": errors,
                "form_name": name,
            },
            status_code=200,
        )

    company = Company(tenant_id=current_user.tenant_id, name=data.name)
    db.add(company)
    db.flush()
    log_audit(
        db,
        "CREATE",
        "company",
        company.id,
        tenant_id=current_user.tenant_id,
        user_id=current_user.id,
    )
    db.commit()
    return RedirectResponse(url="/companies", status_code=303)


@router.get("/companies/{company_id:int}/edit", response_class=HTMLResponse)
def edit_company(
    request: Request,
    company_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_web_user),
) -> HTMLResponse:
    company = _get_company_or_404(db, company_id, current_user.tenant_id)
    if company is None:
        raise HTTPException(status_code=404, detail="Company not found")

    return templates.TemplateResponse(
        "companies/edit.html",
        {"request": request, "company": company, "errors": []},
    )


@router.post("/companies/{company_id:int}")
def update_company(
    request: Request,
    company_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_web_user),
    name: str = Form(""),
    csrf_token: str | None = Form(None),
) -> Response:
    validate_csrf_or_403(request, csrf_token or request.headers.get("X-CSRF-Token"))
    company = _get_company_or_404(db, company_id, current_user.tenant_id)
    if company is None:
        raise HTTPException(status_code=404, detail="Company not found")

    try:
        data = CompanyFormSchema(name=name)
    except ValidationError as e:
        errors = [err["msg"] for err in e.errors()]
        return templates.TemplateResponse(
            "companies/edit.html",
            {
                "request": request,
                "company": company,
                "errors": errors,
                "form_name": name,
            },
            status_code=200,
        )

    company.name = data.name
    company.updated_at = datetime.utcnow()
    log_audit(
        db,
        "UPDATE",
        "company",
        company_id,
        tenant_id=current_user.tenant_id,
        user_id=current_user.id,
    )
    db.commit()
    return RedirectResponse(url="/companies", status_code=303)


@router.post("/companies/{company_id:int}/delete")
def delete_company(
    request: Request,
    company_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_web_user),
    csrf_token: str | None = Form(None),
) -> Response:
    validate_csrf_or_403(request, csrf_token or request.headers.get("X-CSRF-Token"))
    company = _get_company_or_404(db, company_id, current_user.tenant_id)
    if company is None:
        raise HTTPException(status_code=404, detail="Company not found")

    log_audit(
        db,
        "DELETE",
        "company",
        company_id,
        tenant_id=current_user.tenant_id,
        user_id=current_user.id,
    )
    db.delete(company)
    db.commit()

    if request.headers.get("HX-Request") == "true":
        return HTMLResponse(content="", status_code=200)
    return RedirectResponse(url="/companies", status_code=303)
