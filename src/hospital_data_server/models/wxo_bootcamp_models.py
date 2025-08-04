from datetime import date, datetime
from typing import Optional, Dict, List

# Pure Pydantic v2 imports only
from pydantic import BaseModel, Field, model_validator, field_serializer, ConfigDict

from ..wxo_bootcamp_enum_constants import (
    RiskLevel,
    PregnancyCategory,
    InteractionSeverity,
    Gender,
)

# =============================================================================
# PURE PYDANTIC V2 MODELS FOR IBM WATSON ORCHESTRATE
# =============================================================================


class Condition(BaseModel):
    """Medical condition/diagnosis"""

    model_config = ConfigDict(use_enum_values=True, validate_assignment=True, str_strip_whitespace=True)

    condition_id: str = Field(..., min_length=1)
    name: str = Field(..., min_length=1)
    short_name: str = Field(..., min_length=1)
    icd10_code: Optional[str] = Field(default=None, max_length=20)
    severity: RiskLevel = Field(default=RiskLevel.MODERATE)
    chronic: bool = Field(default=False)
    onset_date: Optional[date] = Field(default=None)
    notes: Optional[str] = Field(default=None, max_length=1000)

    @field_serializer("onset_date")
    def serialize_date(self, dt: Optional[date], _info) -> Optional[str]:
        return dt.isoformat() if dt else None


class Allergy(BaseModel):
    """Patient allergy information"""

    model_config = ConfigDict(use_enum_values=True, validate_assignment=True, str_strip_whitespace=True)

    allergen: str = Field(..., min_length=1, max_length=100)
    severity: RiskLevel
    reaction_type: str = Field(
        ...,
        description="Type of reaction: rash, anaphylaxis, nausea, etc.",
        min_length=1,
        max_length=200,
    )
    verified: bool = Field(default=True)
    onset_date: Optional[date] = Field(default=None)

    @field_serializer("onset_date")
    def serialize_date(self, dt: Optional[date], _info) -> Optional[str]:
        return dt.isoformat() if dt else None


class VitalSigns(BaseModel):
    """Patient vital signs and key metrics"""

    model_config = ConfigDict(use_enum_values=True, validate_assignment=True)

    blood_pressure_systolic: Optional[int] = Field(default=None, ge=50, le=300)
    blood_pressure_diastolic: Optional[int] = Field(default=None, ge=30, le=200)
    heart_rate: Optional[int] = Field(default=None, ge=30, le=250)
    weight_kg: Optional[float] = Field(default=None, gt=0, le=500)
    height_cm: Optional[float] = Field(default=None, gt=0, le=300)
    bmi: Optional[float] = Field(default=None, ge=10, le=100)
    creatinine_mg_dl: Optional[float] = Field(default=None, gt=0, description="Kidney function marker")
    creatinine_clearance_ml_min: Optional[float] = Field(default=None, gt=0)
    when: str = Field(
        default_factory=datetime.now().isoformat,
        description="When were these values updated",
    )

    #    @field_serializer("when")
    #    def serialize_datetime(self, dt: datetime, _info) -> str:
    #        return dt.isoformat()

    @model_validator(mode="after")
    def auto_calculate_fields(self):
        """Auto-calculate BMI if not provided"""
        if not self.bmi and self.weight_kg and self.height_cm:
            height_m = self.height_cm / 100
            self.bmi = round(self.weight_kg / (height_m**2), 1)
        return self

    def calculate_bmi(self) -> Optional[float]:
        """Calculate BMI from weight and height"""
        if self.weight_kg and self.height_cm:
            height_m = self.height_cm / 100
            return round(self.weight_kg / (height_m**2), 1)
        return None

    def get_bp_category(self) -> str:
        """Categorize blood pressure reading"""
        if not self.blood_pressure_systolic or not self.blood_pressure_diastolic:
            return "unknown"

        sys, dia = self.blood_pressure_systolic, self.blood_pressure_diastolic
        if sys >= 180 or dia >= 120:
            return "hypertensive_crisis"
        elif sys >= 140 or dia >= 90:
            return "hypertension"
        elif sys >= 130 or dia >= 80:
            return "elevated"
        else:
            return "normal"

    def estimate_creatinine_clearance(self, age: int, sex: Gender):
        """Cockcroft-Gault equation for creatinine clearance estimation"""
        if not self.creatinine_mg_dl or not self.weight_kg:
            return None

        # Cockcroft-Gault: ((140-age) * weight) / (72 * creatinine) * (0.85 if female)
        clearance = ((140 - age) * self.weight_kg) / (72 * self.creatinine_mg_dl)
        if sex == Gender.FEMALE:
            print("FEMALE")
            clearance *= 0.85
        self.creatinine_clearance_ml_min = round(clearance, 1)

    def has_kidney_impairment(self) -> bool:
        """Check if patient has kidney impairment (CrCl <60 mL/min)"""
        return self.creatinine_clearance_ml_min is not None and self.creatinine_clearance_ml_min < 60


class Patient(BaseModel):
    """Patient demographic and clinical information"""

    model_config = ConfigDict(use_enum_values=True, validate_assignment=True, str_strip_whitespace=True)

    patient_id: str = Field(..., min_length=1)
    age: int = Field(..., ge=0, le=150)
    sex: Gender = Field(..., pattern=r"^(M|F|Other)$")
    pregnant: bool = Field(default=False)
    breastfeeding: bool = Field(default=False)
    pregnancy_trimester: Optional[int] = Field(default=None, ge=0, le=3)
    insurance_id: Optional[str] = Field(default=None, description="Anonymized insurance identifier")
    created_date: str = Field(
        default_factory=datetime.now().isoformat,
        description="When was this patient created",
    )

    #    @field_serializer("created_date")
    #    def serialize_datetime(self, dt: datetime, _info) -> str:
    #        return dt.isoformat()

    @model_validator(mode="after")
    def validate_pregnancy_logic(self):
        """Validate pregnancy-related fields"""
        # Only females can be pregnant or breastfeeding
        if self.sex != "F" and (self.pregnant or self.breastfeeding):
            raise ValueError("Only females can be pregnant or breastfeeding")

        # Pregnancy trimester only valid if pregnant
        if self.pregnancy_trimester is not None and self.pregnancy_trimester > 0 and not self.pregnant:
            raise ValueError("Pregnancy trimester only valid if pregnant")

        return self

    def is_elderly(self) -> bool:
        """Check if patient is elderly (≥65 years)"""
        return self.age >= 65

    def is_pediatric(self) -> bool:
        """Check if patient is pediatric (<18 years)"""
        return self.age < 18


class Prescription(BaseModel):
    """Individual drug prescription with API lookup information"""

    model_config = ConfigDict(validate_assignment=True, str_strip_whitespace=True)

    prescription_id: str = Field(..., min_length=1)
    drug_name: str = Field(..., min_length=1, description="Generic name for API lookup")
    brand_name: Optional[str] = Field(default=None, description="The brand name of the drug")
    ndc_code: Optional[str] = Field(default=None, description="National Drug Code")
    rxcui: Optional[str] = Field(default=None, description="RxNorm Concept Unique Identifier")
    dose: str = Field(default="", description="Dosage for the prescription")
    frequency: str = Field(default="", description="How often to take the dose of the drug")
    route: str = Field(default="oral", description="Administration route: oral, IV, topical, etc.")
    duration_days: Optional[int] = Field(default=None, ge=1, description="For how many days to take the drug")
    indication: str = Field(default="")
    prescriber_id: str = Field(default="", description="Anonymized prescriber ID")
    prescriber_notes: str = Field(default="")

    def get_api_search_terms(self) -> List[str]:
        """Get list of search terms for API queries"""
        terms = [self.drug_name]
        if self.brand_name:
            terms.append(self.brand_name)
        return [term for term in terms if term]


class DrugInformation(BaseModel):
    """Structured drug information from API responses"""

    model_config = ConfigDict(validate_assignment=True, use_enum_values=True, str_strip_whitespace=True)

    drug_name: str = Field(..., description="Name of the drug", min_length=1)
    brand_names: Optional[List[str]] = Field(default=None, description="Brand names")
    ndc_codes: List[str] = Field(default_factory=list, description="NDC Codes")
    rxcui: Optional[str] = Field(default=None, description="RxNorm identifier")
    drug_class: Optional[str] = Field(default=None, description="What type of drug is it")
    mechanism: Optional[str] = Field(default=None, description="How it works")
    indications: List[str] = Field(default_factory=list, description="When should you use it")
    contraindications: List[str] = Field(default_factory=list, description="When you should not use it")
    warnings: List[str] = Field(default_factory=list, description="Warnings about the drug")
    pregnancy_category: Optional[PregnancyCategory] = Field(
        default=PregnancyCategory.A,
        description="Can the drug be used on pregnant people",
    )
    controlled_substance: bool = Field(..., description="Is the drug a controlled substance")
    source_apis: List[str] = Field(..., description="Where the info was sourced from")
    last_updated: str = Field(
        default_factory=datetime.now().isoformat,
        description="When were these records updated",
    )


#    @field_serializer("last_updated")
#    def serialize_datetime(self, dt: datetime, _info) -> str:
#        return dt.isoformat()


class DrugInteraction(BaseModel):
    """Drug interaction information"""

    model_config = ConfigDict(use_enum_values=True, validate_assignment=True, str_strip_whitespace=True)

    interaction_id: str = Field(..., description="Unique identifier for the interaction", min_length=1)
    drug1: str = Field(..., description="First drug in the interaction", min_length=1)
    drug2: str = Field(..., description="Second drug in the interaction", min_length=1)
    severity: InteractionSeverity = Field(..., description="Severity level of the interaction")
    mechanism: str = Field(..., description="Mechanism of the drug interaction", min_length=1)
    clinical_effect: str = Field(..., description="Clinical effect of the interaction", min_length=1)
    management: str = Field(..., description="Management recommendations", min_length=1)


class ContraindicationRule(BaseModel):
    """
    Rule defining contraindications for a specific drug

    Represents clinical contraindication rules that specify when a particular drug
    should not be used for certain medical conditions or patient populations.
    """

    model_config = ConfigDict(
        use_enum_values=True,
        validate_assignment=True,
        str_strip_whitespace=True,
        json_schema_extra={
            "examples": [
                {
                    "rule_id": "CONTRA001",
                    "drug": "warfarin",
                    "condition": "pregnancy",
                    "severity": "critical",
                    "reason": "Teratogenic - causes fetal warfarin syndrome",
                }
            ]
        },
    )

    rule_id: str = Field(
        ...,
        description="Unique identifier for the contraindication rule",
        min_length=1,
        max_length=50,
    )
    drug: str = Field(
        ...,
        description="Drug name (generic name preferred)",
        min_length=1,
        max_length=100,
    )
    condition: str = Field(
        ...,
        description="Medical condition or patient population where drug is contraindicated",
        min_length=1,
        max_length=200,
    )
    severity: RiskLevel = Field(
        ...,
        description="Risk level of the contraindication (low, moderate, high, critical)",
    )
    reason: str = Field(
        ...,
        description="Clinical reason explaining why the drug is contraindicated",
        min_length=1,
        max_length=500,
    )

    def is_critical(self) -> bool:
        """Check if this contraindication is critical severity"""
        return self.severity == RiskLevel.CRITICAL

    def get_summary(self) -> str:
        """Get a human-readable summary of the contraindication"""
        return f"{self.drug.title()} is contraindicated in {self.condition} ({self.severity} risk): {self.reason}"


class AlternativeDrug(BaseModel):
    """Alternative drug information"""

    model_config = ConfigDict(validate_assignment=True, str_strip_whitespace=True)

    rationale: str = Field(..., description="Rationale for the alternative", min_length=1)
    safety_improvement: str = Field(..., description="How safety is improved", min_length=1)
    efficacy_comparison: str = Field(..., description="Efficacy comparison with original drug", min_length=1)


class AlternativeTreatment(BaseModel):
    """Alternative treatment options for a drug"""

    model_config = ConfigDict(validate_assignment=True, str_strip_whitespace=True)

    original_drug: str = Field(..., description="Original drug being replaced", min_length=1)
    alternatives: Dict[str, AlternativeDrug] = Field(..., description="Dictionary of alternative drugs")
    conditions: List[str] = Field(..., description="Conditions where alternatives are recommended")


class MedicalServerOutput(BaseModel):
    """
    Groups data about a patient's Conditions (diagnoses), Allergies and Prescriptions
    """

    model_config = ConfigDict(validate_assignment=True, use_enum_values=True, str_strip_whitespace=True)

    conditions: List[str] = Field(
        default_factory=list,
        description="Conditions, Diagnoses, Diseases a patient has, blank if none",
    )
    allergies: List[Allergy] = Field(
        default_factory=list,
        description="List of allergies a patient has, blank if none",
    )
    prescriptions: List[Prescription] = Field(default_factory=list, description="List of prescriptions a patient has")


class Patient360(BaseModel):
    """A comprehensive view of a patient collecting data from different servers"""

    model_config = ConfigDict(validate_assignment=True, use_enum_values=True)

    information: Optional[Patient] = Field(description="Basic information about a patient")
    medical: Optional[MedicalServerOutput] = Field(description="List of conditions, allergies and prescriptions a patient has")
    vital_signs: Optional[VitalSigns] = Field(description="Most recent vital signs of a patient")

    @model_validator(mode="after")
    def auto_calculate_vitals(self):
        """Auto-calculate vital sign derived values"""
        if self.information and self.vital_signs and self.information.age and self.information.sex:
            # Auto-calculate creatinine clearance if not provided
            if not self.vital_signs.creatinine_clearance_ml_min and self.vital_signs.creatinine_mg_dl and self.vital_signs.weight_kg:
                clearance = ((140 - self.information.age) * self.vital_signs.weight_kg) / (72 * self.vital_signs.creatinine_mg_dl)
                if self.information.sex.upper() == "F":
                    clearance *= 0.85
                self.vital_signs.creatinine_clearance_ml_min = round(clearance, 1)

        return self

    # def to_api_query_context(self) -> Dict[str, Any]:
    #     """Convert patient data to context for API queries"""
    #     return {
    #         "age": self.information.age,
    #         "sex": self.information.sex,
    #         "pregnant": self.information.pregnant,
    #         "breastfeeding": self.information.breastfeeding,
    #         "pregnancy_trimester": self.information.pregnancy_trimester,
    #         "elderly": self.information.is_elderly(),
    #         "pediatric": self.information.is_pediatric(),
    #         "kidney_impaired": self.vital_signs.has_kidney_impairment(),
    #         "conditions": list(self.medical.conditions),
    #         "allergies": list(self.medical.allergies),
    #         "vital_signs": self.vital_signs.model_dump() if self.vital_signs else None,
    #     }
