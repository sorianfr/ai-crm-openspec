"""Company CRUD routes."""

from datetime import datetime

from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse, Response
from pydantic import ValidationError
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.templates import templates
from app.db.session import get_db
from app.models import Company
from app.schemas.company import CompanyFormSchema

router = APIRouter()


def _get_company_or_404(db: Session, company_id: int) -> Company | None:
    return db.get(Company, company_id)


@router.get("/companies", response_class=HTMLResponse)
def list_companies(request: Request, db: Session = Depends(get_db)) -> HTMLResponse:
    companies = db.execute(select(Company).order_by(Company.name.asc())).scalars().all()
    return templates.TemplateResponse(
        "companies/list.html",
        {"request": request, "companies": companies},
    )


@router.get("/companies/new", response_class=HTMLResponse)
def new_company(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        "companies/new.html",
        {"request": request, "errors": []},
    )


@router.post("/companies")
def create_company(
    request: Request,
    db: Session = Depends(get_db),
    name: str = Form(""),
) -> Response:
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

    company = Company(name=data.name)
    db.add(company)
    db.commit()
    return RedirectResponse(url="/companies", status_code=303)


@router.get("/companies/{company_id:int}/edit", response_class=HTMLResponse)
def edit_company(
    request: Request,
    company_id: int,
    db: Session = Depends(get_db),
) -> HTMLResponse:
    company = _get_company_or_404(db, company_id)
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
    name: str = Form(""),
) -> Response:
    company = _get_company_or_404(db, company_id)
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
    db.commit()
    return RedirectResponse(url="/companies", status_code=303)


@router.post("/companies/{company_id:int}/delete")
def delete_company(
    request: Request,
    company_id: int,
    db: Session = Depends(get_db),
) -> Response:
    company = _get_company_or_404(db, company_id)
    if company is None:
        raise HTTPException(status_code=404, detail="Company not found")

    db.delete(company)
    db.commit()

    if request.headers.get("HX-Request") == "true":
        return HTMLResponse(content="", status_code=200)
    return RedirectResponse(url="/companies", status_code=303)
