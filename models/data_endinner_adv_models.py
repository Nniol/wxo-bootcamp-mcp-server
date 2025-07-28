from typing import List, Dict

from pydantic import BaseModel, Field


class PatientData(BaseModel):
    patient_id: int = Field(description="The patient's unique identifier.")
    name: str = Field(description="The patient's name")
    age: int = Field(description="The patienbt's age")
    sex: str = Field(description="The patient's gender")
    zip_code: int = Field(description="The patient's zip code")
    personality: str = Field(
        description="The personality of the patient. Used when generating transcripts"
    )


class VisitData(BaseModel):
    patient_id: int = Field(description="The patient's unique identifier.")
    visit_id: int = Field(description="The unique ID of the visit")
    date: str = Field(description="Date of the visit")
    chief_complaint: str = Field(description="Why did the patient visit the doctor")
    tests: Dict[str, str] = Field(
        default_factory=dict,
        description="The tests performed and the result of the test",
    )
    diagnosis_from_test: str = Field(description="Which test enabled the diagnosis")
    diagnosis: str = Field(description="The diagnosis made by the doctor")
    treatment: str = Field(description="How is the diagnosis to be treated")
    medicines: List[str] = Field(description="What medicines to be used")
    painkillers: List[str] = Field(description="What painkillers to use")
    antibiotics: List[str] = Field(description="What antibiotics to use")
    died: bool = Field(description="Did the paitient die from their diagnosis")
