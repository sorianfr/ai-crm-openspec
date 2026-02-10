"""Contact CRUD routes. Forms are application/x-www-form-urlencoded; use Form(...); validate with Pydantic; on validation errors re-render template (HTTP 200)."""

from datetime import datetime

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse, Response
from pydantic import ValidationError
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.templates import templates
from app.db.session import get_db
from app.models import Contact
from app.schemas.contact import ContactFormSchema

router = APIRouter()


def _get_contact_or_404(db: Session, contact_id: int) -> Contact | None:
    return db.get(Contact, contact_id)


@router.get("/contacts", response_class=HTMLResponse)
def list_contacts(
    request: Request,
    db: Session = Depends(get_db),
) -> HTMLResponse:
    contacts = (
        db.execute(select(Contact).order_by(Contact.updated_at.desc()))
        .scalars()
        .all()
    )
    return templates.TemplateResponse(
        "contacts/list.html",
        {"request": request, "contacts": contacts},
    )


@router.get("/contacts/new", response_class=HTMLResponse)
def new_contact(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        "contacts/new.html",
        {"request": request, "contact": None, "errors": []},
    )


@router.post("/contacts")
def create_contact(
    request: Request,
    db: Session = Depends(get_db),
    full_name: str = Form(""),
    email: str | None = Form(None),
    phone: str | None = Form(None),
    company: str | None = Form(None),
) -> Response:
    try:
        data = ContactFormSchema(
            full_name=full_name.strip(),
            email=email.strip() if email else None,
            phone=phone.strip() if phone else None,
            company=company.strip() if company else None,
        )
    except ValidationError as e:
        errors = [err["msg"] for err in e.errors()]
        return templates.TemplateResponse(
            "contacts/new.html",
            {
                "request": request,
                "contact": None,
                "errors": errors,
                "form_full_name": full_name,
                "form_email": email or "",
                "form_phone": phone or "",
                "form_company": company or "",
            },
            status_code=200,
        )
    contact = Contact(
        full_name=data.full_name,
        email=data.email,
        phone=data.phone,
        company=data.company,
    )
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return RedirectResponse(url="/contacts", status_code=303)


@router.get("/contacts/{contact_id:int}/edit", response_class=HTMLResponse)
def edit_contact(
    request: Request,
    contact_id: int,
    db: Session = Depends(get_db),
) -> HTMLResponse:
    contact = _get_contact_or_404(db, contact_id)
    if contact is None:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Contact not found")
    return templates.TemplateResponse(
        "contacts/edit.html",
        {"request": request, "contact": contact, "errors": []},
    )


@router.post("/contacts/{contact_id:int}")
def update_contact(
    request: Request,
    contact_id: int,
    db: Session = Depends(get_db),
    full_name: str = Form(""),
    email: str | None = Form(None),
    phone: str | None = Form(None),
    company: str | None = Form(None),
) -> Response:
    contact = _get_contact_or_404(db, contact_id)
    if contact is None:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Contact not found")
    try:
        data = ContactFormSchema(
            full_name=full_name.strip(),
            email=email.strip() if email else None,
            phone=phone.strip() if phone else None,
            company=company.strip() if company else None,
        )
    except ValidationError as e:
        errors = [err["msg"] for err in e.errors()]
        return templates.TemplateResponse(
            "contacts/edit.html",
            {
                "request": request,
                "contact": contact,
                "errors": errors,
                "form_full_name": full_name,
                "form_email": email or "",
                "form_phone": phone or "",
                "form_company": company or "",
            },
            status_code=200,
        )
    contact.full_name = data.full_name
    contact.email = data.email
    contact.phone = data.phone
    contact.company = data.company
    contact.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(contact)
    return RedirectResponse(url="/contacts", status_code=303)


@router.post("/contacts/{contact_id:int}/delete")
def delete_contact(
    contact_id: int,
    db: Session = Depends(get_db),
):
    contact = _get_contact_or_404(db, contact_id)
    if contact is None:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Contact not found")
    db.delete(contact)
    db.commit()
    return HTMLResponse(content="", status_code=200)
