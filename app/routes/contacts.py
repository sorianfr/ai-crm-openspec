"""Contact CRUD routes. Forms are application/x-www-form-urlencoded; use Form(...); validate with Pydantic; on validation errors re-render template (HTTP 200)."""

from datetime import datetime

from fastapi import APIRouter, Depends, Form, HTTPException, Query, Request
from fastapi.responses import HTMLResponse, RedirectResponse, Response
from pydantic import ValidationError
from sqlalchemy import or_, select
from sqlalchemy.orm import Session, selectinload

from app.core.templates import templates
from app.db.session import get_db
from app.models import Activity, Company, Contact, Note
from app.schemas.activity import ActivityFormSchema
from app.schemas.contact import ContactFormSchema
from app.schemas.note import NoteFormSchema

router = APIRouter()


def _get_contact_or_404(db: Session, contact_id: int) -> Contact | None:
    return db.get(Contact, contact_id)


def _list_companies(db: Session) -> list[Company]:
    return db.execute(select(Company).order_by(Company.name.asc())).scalars().all()


def _resolve_company_id(
    db: Session,
    company_id_raw: str | None,
) -> tuple[int | None, str | None]:
    if company_id_raw is None or company_id_raw.strip() == "":
        return None, None
    try:
        company_id = int(company_id_raw)
    except ValueError:
        return None, "Selected company is invalid"

    company = db.get(Company, company_id)
    if company is None:
        return None, "Selected company is invalid"
    return company_id, None


def _resolve_or_create_company(
    db: Session,
    name: str | None,
) -> tuple[Company | None, str | None]:
    """Resolve company by name (case-insensitive) or create. Returns (Company, None) or (None, error)."""
    normalized = (name or "").strip()
    if not normalized:
        return None, "Company name is required"
    existing = (
        db.execute(select(Company).where(Company.name.ilike(normalized)).limit(1))
        .scalars()
        .first()
    )
    if existing is not None:
        return existing, None
    company = Company(name=normalized)
    db.add(company)
    db.flush()
    return company, None


@router.get("/contacts", response_class=HTMLResponse)
def list_contacts(
    request: Request,
    q: str = Query(default=""),
    has_email: bool = Query(default=False),
    has_phone: bool = Query(default=False),
    db: Session = Depends(get_db),
) -> HTMLResponse:
    stmt = select(Contact).options(selectinload(Contact.company_ref))

    q = q.strip()
    if q:
        search_value = f"%{q}%"
        stmt = stmt.where(
            or_(
                Contact.full_name.ilike(search_value),
                Contact.email.ilike(search_value),
                Contact.company.ilike(search_value),
            )
        )

    if has_email:
        stmt = stmt.where(Contact.email.is_not(None), Contact.email != "")

    if has_phone:
        stmt = stmt.where(Contact.phone.is_not(None), Contact.phone != "")

    contacts = (
        db.execute(stmt.order_by(Contact.updated_at.desc()))
        .scalars()
        .all()
    )
    context = {
        "request": request,
        "contacts": contacts,
        "q": q,
        "has_email": has_email,
        "has_phone": has_phone,
    }

    if request.headers.get("HX-Request"):
        return templates.TemplateResponse("contacts/_contacts_table.html", context)

    return templates.TemplateResponse("contacts/list.html", context)


@router.get("/contacts/new", response_class=HTMLResponse)
def new_contact(
    request: Request,
    db: Session = Depends(get_db),
) -> HTMLResponse:
    return templates.TemplateResponse(
        "contacts/new.html",
        {
            "request": request,
            "contact": None,
            "errors": [],
            "companies": _list_companies(db),
        },
    )


@router.post("/contacts")
def create_contact(
    request: Request,
    db: Session = Depends(get_db),
    full_name: str = Form(""),
    email: str | None = Form(None),
    phone: str | None = Form(None),
    company: str | None = Form(None),
    company_id: str | None = Form(None),
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
                "form_company_id": company_id or "",
                "companies": _list_companies(db),
            },
            status_code=200,
        )
    company_text = (company or "").strip()
    if company_text:
        resolved_company, resolve_error = _resolve_or_create_company(db, company_text)
        if resolve_error:
            return templates.TemplateResponse(
                "contacts/new.html",
                {
                    "request": request,
                    "contact": None,
                    "errors": [resolve_error],
                    "form_full_name": full_name,
                    "form_email": email or "",
                    "form_phone": phone or "",
                    "form_company": company or "",
                    "form_company_id": company_id or "",
                    "companies": _list_companies(db),
                },
                status_code=200,
            )
        selected_company_id = resolved_company.id
        company_display_name = resolved_company.name
    else:
        selected_company_id, company_id_error = _resolve_company_id(db, company_id)
        if company_id_error:
            return templates.TemplateResponse(
                "contacts/new.html",
                {
                    "request": request,
                    "contact": None,
                    "errors": [company_id_error],
                    "form_full_name": full_name,
                    "form_email": email or "",
                    "form_phone": phone or "",
                    "form_company": company or "",
                    "form_company_id": company_id or "",
                    "companies": _list_companies(db),
                },
                status_code=200,
            )
        company_display_name = None
        if selected_company_id is not None:
            c = db.get(Company, selected_company_id)
            company_display_name = c.name if c else None
    contact = Contact(
        full_name=data.full_name,
        email=data.email,
        phone=data.phone,
        company=company_display_name if company_display_name is not None else data.company,
        company_id=selected_company_id,
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
    contact = (
        db.execute(
            select(Contact)
            .where(Contact.id == contact_id)
            .options(selectinload(Contact.company_ref))
        )
        .unique()
        .scalar_one_or_none()
    )
    if contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    notes = (
        db.execute(
            select(Note).where(Note.contact_id == contact_id).order_by(Note.created_at.desc())
        )
        .scalars()
        .all()
    )
    activities = (
        db.execute(
            select(Activity)
            .where(Activity.contact_id == contact_id)
            .order_by(Activity.activity_date.desc())
        )
        .scalars()
        .all()
    )
    return templates.TemplateResponse(
        "contacts/edit.html",
        {
            "request": request,
            "contact": contact,
            "notes": notes,
            "activities": activities,
            "errors": [],
            "companies": _list_companies(db),
        },
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
    company_id: str | None = Form(None),
) -> Response:
    contact = _get_contact_or_404(db, contact_id)
    if contact is None:
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
        notes = (
            db.execute(
                select(Note).where(Note.contact_id == contact_id).order_by(Note.created_at.desc())
            )
            .scalars()
            .all()
        )
        activities = (
            db.execute(
                select(Activity)
                .where(Activity.contact_id == contact_id)
                .order_by(Activity.activity_date.desc())
            )
            .scalars()
            .all()
        )
        return templates.TemplateResponse(
            "contacts/edit.html",
            {
                "request": request,
                "contact": contact,
                "notes": notes,
                "activities": activities,
                "errors": errors,
                "form_full_name": full_name,
                "form_email": email or "",
                "form_phone": phone or "",
                "form_company": company or "",
                "form_company_id": company_id or "",
                "companies": _list_companies(db),
            },
            status_code=200,
        )
    company_text = (company or "").strip()
    if company_text:
        resolved_company, resolve_error = _resolve_or_create_company(db, company_text)
        if resolve_error:
            notes = (
                db.execute(
                    select(Note).where(Note.contact_id == contact_id).order_by(Note.created_at.desc())
                )
                .scalars()
                .all()
            )
            activities = (
                db.execute(
                    select(Activity)
                    .where(Activity.contact_id == contact_id)
                    .order_by(Activity.activity_date.desc())
                )
                .scalars()
                .all()
            )
            return templates.TemplateResponse(
                "contacts/edit.html",
                {
                    "request": request,
                    "contact": contact,
                    "notes": notes,
                    "activities": activities,
                    "errors": [resolve_error],
                    "form_full_name": full_name,
                    "form_email": email or "",
                    "form_phone": phone or "",
                    "form_company": company or "",
                    "form_company_id": company_id or "",
                    "companies": _list_companies(db),
                },
                status_code=200,
            )
        selected_company_id = resolved_company.id
        company_display_name = resolved_company.name
    else:
        selected_company_id, company_id_error = _resolve_company_id(db, company_id)
        if company_id_error:
            notes = (
                db.execute(
                    select(Note).where(Note.contact_id == contact_id).order_by(Note.created_at.desc())
                )
                .scalars()
                .all()
            )
            activities = (
                db.execute(
                    select(Activity)
                    .where(Activity.contact_id == contact_id)
                    .order_by(Activity.activity_date.desc())
                )
                .scalars()
                .all()
            )
            return templates.TemplateResponse(
                "contacts/edit.html",
                {
                    "request": request,
                    "contact": contact,
                    "notes": notes,
                    "activities": activities,
                    "errors": [company_id_error],
                    "form_full_name": full_name,
                    "form_email": email or "",
                    "form_phone": phone or "",
                    "form_company": company or "",
                    "form_company_id": company_id or "",
                    "companies": _list_companies(db),
                },
                status_code=200,
            )
        company_display_name = None
        if selected_company_id is not None:
            c = db.get(Company, selected_company_id)
            company_display_name = c.name if c else None
    contact.full_name = data.full_name
    contact.email = data.email
    contact.phone = data.phone
    contact.company = company_display_name if company_display_name is not None else data.company
    contact.company_id = selected_company_id
    contact.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(contact)
    return RedirectResponse(url="/contacts", status_code=303)


@router.post("/contacts/{contact_id:int}/notes")
def create_note(
    request: Request,
    contact_id: int,
    db: Session = Depends(get_db),
    content: str = Form(""),
) -> Response:
    contact = _get_contact_or_404(db, contact_id)
    if contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    try:
        data = NoteFormSchema(content=content)
    except ValidationError as e:
        note_errors = [err["msg"] for err in e.errors()]
        fragment = templates.TemplateResponse(
            "contacts/_add_note_form_container.html",
            {
                "request": request,
                "contact": contact,
                "note_errors": note_errors,
                "form_content": content,
            },
        )
        fragment.headers["HX-Retarget"] = "#add-note-form-container"
        fragment.headers["HX-Reswap"] = "outerHTML"
        return fragment
    note = Note(contact_id=contact_id, content=data.content)
    db.add(note)
    db.commit()
    db.refresh(note)
    fragment = templates.TemplateResponse(
        "contacts/_note_row.html",
        {"request": request, "note": note},
    )
    return fragment


@router.post("/contacts/{contact_id:int}/activities")
def create_activity(
    request: Request,
    contact_id: int,
    db: Session = Depends(get_db),
    type: str = Form(""),
    description: str = Form(""),
    activity_date: str = Form(""),
) -> Response:
    contact = _get_contact_or_404(db, contact_id)
    if contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    try:
        data = ActivityFormSchema(
            type=type.strip(),
            description=description,
            activity_date=activity_date,
        )
    except ValidationError as e:
        activity_errors = [err["msg"] for err in e.errors()]
        fragment = templates.TemplateResponse(
            "contacts/_add_activity_form_container.html",
            {
                "request": request,
                "contact": contact,
                "activity_errors": activity_errors,
                "form_type": type,
                "form_description": description,
                "form_activity_date": activity_date,
            },
        )
        fragment.headers["HX-Retarget"] = "#add-activity-form-container"
        fragment.headers["HX-Reswap"] = "outerHTML"
        return fragment
    activity = Activity(
        contact_id=contact_id,
        type=data.type,
        description=data.description,
        activity_date=data.activity_date,
    )
    db.add(activity)
    db.commit()
    db.refresh(activity)
    fragment = templates.TemplateResponse(
        "contacts/_activity_row.html",
        {"request": request, "activity": activity},
    )
    return fragment


@router.post("/activities/{activity_id:int}/delete")
def delete_activity(
    activity_id: int,
    db: Session = Depends(get_db),
) -> HTMLResponse:
    activity = db.get(Activity, activity_id)
    if activity is None:
        raise HTTPException(status_code=404, detail="Activity not found")
    db.delete(activity)
    db.commit()
    return HTMLResponse(content="", status_code=200)


@router.post("/notes/{note_id:int}/delete")
def delete_note(
    note_id: int,
    db: Session = Depends(get_db),
) -> HTMLResponse:
    note = db.get(Note, note_id)
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    db.delete(note)
    db.commit()
    return HTMLResponse(content="", status_code=200)


@router.post("/contacts/{contact_id:int}/delete")
def delete_contact(
    contact_id: int,
    db: Session = Depends(get_db),
):
    contact = _get_contact_or_404(db, contact_id)
    if contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    db.delete(contact)
    db.commit()
    return HTMLResponse(content="", status_code=200)
