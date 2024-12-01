from fastapi import Depends, HTTPException
from sqlmodel import Session, select
from app.models import LicenseApplication
from app.schema import CreateDraft, SubmitApplication, LicenseApplicationResponse, LicenseApplicationList
from app.database import get_session

def save_draft(session: Session, data: CreateDraft):
    """
    Save a draft license application.
    """
    draft = LicenseApplication(**data.dict())
    session.add(draft)
    session.commit()
    session.refresh(draft)
    return draft

def submit_application(session: Session, application_id: int, data: SubmitApplication):
    """
    Submit a draft application by updating its status to 'submitted'.
    """
    application = session.get(LicenseApplication, application_id)
    if not application or application.status != "draft":
        raise HTTPException(status_code=404, detail="Application not found or not in draft status.")
    
    for key, value in data.model_dump().items():
        setattr(application, key, value)
    application.status = "submitted"
    session.add(application)
    session.commit()
    session.refresh(application)
    return application

def get_all_applications(session: Session):
    """
    Retrieve all license applications from the database.
    """
    applications = session.exec(select(LicenseApplication)).all()
    return applications

def get_application_by_id(session: Session, application_id: int):
    """
    Retrieve a specific license application by its ID.
    """
    application = session.get(LicenseApplication, application_id)
    if not application:
        raise HTTPException(status_code=404, detail="Application not found.")
    return application

def delete_application(session: Session, application_id: int):
    """
    Delete a license application by its ID.
    """
    application = session.get(LicenseApplication, application_id)
    if not application:
        raise HTTPException(status_code=404, detail="Application not found.")
    session.delete(application)
    session.commit()
    return {"detail": "Application deleted successfully."}