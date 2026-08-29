
from fastapi import APIRouter, Depends
from app.auth.firebase_middleware import get_current_caregiver_id
from app.models.reminder import ReminderCreate, ReminderStatusUpdate, ReminderOut
from app.services import firestore_service as fs
from app.services.engagement_calc import recompute_engagement

router = APIRouter(prefix="/api/patients/{patient_id}/reminders", tags=["reminders"])


@router.post("", status_code=201)
def create_reminder(
    patient_id: str,
    body: ReminderCreate,
    caregiver_id: str = Depends(get_current_caregiver_id),
):
    """Create a new medicine or activity reminder."""
    reminder_id = fs.create_reminder(caregiver_id, patient_id, body.model_dump())
    return {"reminderId": reminder_id}


@router.get("", status_code=200)
def list_reminders(
    patient_id: str,
    caregiver_id: str = Depends(get_current_caregiver_id),
):
    """List all reminders for a patient."""
    return fs.get_reminders(caregiver_id, patient_id)


@router.patch("/{reminder_id}", status_code=200)
def update_reminder_status(
    patient_id: str,
    reminder_id: str,
    body: ReminderStatusUpdate,
    caregiver_id: str = Depends(get_current_caregiver_id),
):
    """
    Update reminder status (completed / missed / pending).
    Triggers engagement summary recompute so adherence rate stays fresh.
    Called by reminder UI or local device scheduler.
    """
    fs.update_reminder(caregiver_id, patient_id, reminder_id, body.model_dump())
    summary = recompute_engagement(caregiver_id, patient_id)
    return {"status": "updated", "engagementSummary": summary.model_dump()}

=======
from typing import List, Optional
from fastapi import APIRouter, HTTPException, status, Query
from app.database.db import db
from app.schemas import ReminderCreate, ReminderUpdate, ReminderResponse
from app.services.reminder_service import ReminderService

router = APIRouter(tags=["Reminders"])

@router.post("/api/reminders", response_model=ReminderResponse, status_code=status.HTTP_201_CREATED)
@router.post("/reminders", response_model=ReminderResponse, status_code=status.HTTP_201_CREATED)
def create_reminder(reminder_in: ReminderCreate):
    """Creates a new scheduled reminder for a dementia patient (medication, games, hydration, routine)."""
    patient = db.patients.find_one({"id": reminder_in.patient_id})
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Patient with ID '{reminder_in.patient_id}' not found."
        )

    doc = ReminderService.create_reminder(reminder_in)
    return ReminderResponse(**doc)

@router.get("/api/reminders/patient/{patient_id}", response_model=List[ReminderResponse])
@router.get("/reminders/patient/{patient_id}", response_model=List[ReminderResponse])
def get_patient_reminders(patient_id: str, include_completed: bool = Query(True)):
    """Lists all reminders for a specific patient."""
    patient = db.patients.find_one({"id": patient_id})
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Patient with ID '{patient_id}' not found."
        )

    reminders = ReminderService.get_patient_reminders(patient_id, include_completed=include_completed)
    return [ReminderResponse(**r) for r in reminders]

@router.get("/api/reminders/{reminder_id}", response_model=ReminderResponse)
def get_reminder(reminder_id: str):
    """Retrieves reminder details by reminder ID."""
    doc = ReminderService.get_reminder(reminder_id)
    if not doc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Reminder with ID '{reminder_id}' not found."
        )
    return ReminderResponse(**doc)

@router.put("/api/reminders/{reminder_id}", response_model=ReminderResponse)
def update_reminder(reminder_id: str, updates_in: ReminderUpdate):
    """Updates a reminder."""
    doc = ReminderService.update_reminder(reminder_id, updates_in)
    if not doc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Reminder with ID '{reminder_id}' not found."
        )
    return ReminderResponse(**doc)

@router.delete("/api/reminders/{reminder_id}", status_code=status.HTTP_200_OK)
def delete_reminder(reminder_id: str):
    """Deletes a scheduled reminder."""
    deleted = ReminderService.delete_reminder(reminder_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Reminder with ID '{reminder_id}' not found."
        )
    return {"success": True, "message": f"Reminder '{reminder_id}' deleted successfully."}

@router.patch("/api/reminders/{reminder_id}/complete", response_model=ReminderResponse)
def toggle_reminder_completion(reminder_id: str, completed: bool = Query(True)):
    """Marks a reminder as completed or pending."""
    doc = ReminderService.mark_completed(reminder_id, completed=completed)
    if not doc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Reminder with ID '{reminder_id}' not found."
        )
    return ReminderResponse(**doc)

