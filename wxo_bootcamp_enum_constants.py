from enum import Enum

# =============================================================================
# ENUMS AND CONSTANTS
# =============================================================================


class RiskLevel(str, Enum):
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    CRITICAL = "critical"


class PregnancyCategory(str, Enum):
    A = "Safe"
    B = "Probably safe"
    C = "Risk cannot be ruled out"
    D = "Positive evidence of risk"
    X = "Contraindicated"


class InteractionSeverity(str, Enum):
    MINOR = "minor"
    MODERATE = "moderate"
    MAJOR = "major"
    CONTRAINDICATED = "contraindicated"


class PatientStatus(str, Enum):
    STABLE = "stable"
    MONITORING_REQUIRED = "monitoring_required"
    URGENT_REVIEW = "urgent_review"
    CRITICAL = "critical"


class Gender(str, Enum):
    FEMALE = "F"
    MALE = "M"
    OTHER = "OTHER"
