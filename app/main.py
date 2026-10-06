from uuid import uuid4

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from app.classifier import classify_complaint
from app.masking import mask_personal_data
from app.rules import TEAM_BY_CATEGORY, has_fraud_terms

app = FastAPI()


class TriageRequest(BaseModel):
    complaint: str


@app.post("/triage")
def triage(request: TriageRequest) -> dict[str, object]:
    complaint = request.complaint
    if len(complaint) < 20:
        raise HTTPException(
            status_code=422,
            detail="Please enter the full complaint (at least 20 characters).",
        )
    if len(complaint) > 2000:
        raise HTTPException(
            status_code=422,
            detail="Complaint must be 2,000 characters or fewer.",
        )

    masked_text = mask_personal_data(complaint)
    fraud_rule_applied = has_fraud_terms(complaint)
    try:
        classification = classify_complaint(masked_text)
    except RuntimeError as error:
        raise HTTPException(status_code=503, detail=str(error)) from error
    except Exception as error:
        raise HTTPException(status_code=502, detail="Gemini classification failed.") from error

    if classification is None:
        return {
            "complaint_id": str(uuid4()),
            "masked_text": masked_text,
            "category": None,
            "urgency": "High" if fraud_rule_applied else None,
            "team": None,
            "reason": None,
            "fraud_rule_applied": fraud_rule_applied,
            "status": "Needs manual review",
        }

    category = classification["category"]
    urgency = "High" if fraud_rule_applied else classification["urgency"]
    return {
        "complaint_id": str(uuid4()),
        "masked_text": masked_text,
        "category": category,
        "urgency": urgency,
        "team": TEAM_BY_CATEGORY[category],
        "reason": classification["reason"],
        "fraud_rule_applied": fraud_rule_applied,
        "status": "Urgency raised by fraud rule" if fraud_rule_applied else "Success",
    }