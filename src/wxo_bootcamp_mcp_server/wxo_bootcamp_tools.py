import asyncio
import logging

from typing import Dict, Optional


from fastmcp.server import Context
from fastmcp.server import FastMCP
# from mcp.types import SamplingMessage, TextContent

from .data.wxo_bootcamp_data import (
    SAMPLE_BED_SIDE_DATA_SERVER,
    SAMPLE_MEDICAL_SERVER,
    SAMPLE_PATIENTS,
    DRUG_DATABASE,
    DRUG_INTERACTIONS,
    CONTRAINDICATION_RULES,
    ALTERNATIVE_TREATMENTS,
)

from .models.wxo_bootcamp_models import (
    AlternativeTreatment,
    ContraindicationRule,
    Patient,
    DrugInformation,
    DrugInteraction,
    MedicalServerOutput,
    Patient360,
    VitalSigns,
)
from .util.pydantic_to_mcp import pydantic_to_mcp_schema
from .wxo_bootcamp_enum_constants import Gender

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filename="mcp_server.log",
)
log = logging.getLogger("MCPServer")
# log.setLevel(logging.DEBUG)

# PROJECT_ROOT = Path(__file__).resolve().parent

mcp = FastMCP("wxo-bootcamp-mcp-server")

@mcp.tool(
    name="wxoGetVitalSignsInformation",
    description="Returns patient vital signs from the bedside system (Blood pressure, pulse, creatine data, bmi, weight, height) or None.",
    output_schema=pydantic_to_mcp_schema(VitalSigns),
)
def wxobc_get_vital_signs_data_tool(patient_id: str, age: int, sex: str) -> Optional[VitalSigns]:
    """
    Retrieves patient vital signs data for a given patient id.

    This function fetches comprehensive vital sign data for a patient

    Args:
        patient_id (str): The unique patient identifier. Must be a valid patient ID
                        in the format 'PAT' followed by 3 digits (e.g., 'PAT123').
        age: the age of the patient
        sex: The gender of the patient a single string, either F for Female, or M for Male or OTHER

    Returns:
        Optional [VitalSigns]: If a record for patient (patient_id exists)
    """
    enum_sex = Gender(sex)
    vs: Optional[VitalSigns] = SAMPLE_BED_SIDE_DATA_SERVER.get(patient_id)
    if vs:
        vs.estimate_creatinine_clearance(age, enum_sex)
    return vs


@mcp.tool(
    name="wxoGetPatientInformation",
    description="Returns basic patient information from the healthcare database including personal details, contact information and insurance data or None.",
    output_schema=pydantic_to_mcp_schema(Patient),
)
def wxobc_get_patient_information_tool(
    patient_id: str,
) -> Optional[Patient]:
    """
    Retrieves basic patient information by patient ID.

    This function fetches bsaic patient information from the healthcare database
    including personal details, contact information and insurance data.

    Args:
        patient_id (str): The unique patient identifier. Must be a valid patient ID
                        in the format 'PAT' followed by 3 digits (e.g., 'PAT123').

    Returns:
        Optional [Patient]: If a record for patient (patient_id exists)

    """
    return SAMPLE_PATIENTS.get(patient_id)


@mcp.tool(
    name="wxoGetMedicalInformation",
    description="Returns comprehensive patient medical inforamation regarding the diagnosis (condition), allergies and any given prescriptions or None",
    output_schema=pydantic_to_mcp_schema(MedicalServerOutput),
)
def wxobc_get_medical_information_tool(
    patient_id: str,
) -> Optional[MedicalServerOutput]:
    """
    Retrieves patient diagnosis (conditions), allergies and prescription

    This function fetches comprehensive patient medical inforamation regarding the diagnosis (condition), allergies and
    any given prescriptions

    Args:
        patient_id (str): The unique patient identifier. Must be a valid patient ID
                        in the format 'PAT' followed by 3 digits (e.g., 'PAT123').

    Returns:
        Optional [MedicalServerOutput]: If a record for patient (patient_id exists)
    """
    return SAMPLE_MEDICAL_SERVER.get(patient_id)


@mcp.tool(
    name="wxoGetDrugInformation",
    description="Returns comprehensive drug medical inforamation for a given drug or None",
    output_schema=pydantic_to_mcp_schema(DrugInformation),
)
def wxobc_get_drug_data_from_name_tool(drug_name: str) -> Optional[DrugInformation]:
    """
    Retrieves information about a drug

    This function fetches comprehensive drug medical inforamation

    Args:
        drug_name (str): The unique name of the drug

    Returns:
        Optional[DrugInformation]: If a record exists for the drug
    """
    return DRUG_DATABASE.get(drug_name.lower())


@mcp.tool(
    name="wxoGetDrugInterations",
    description="Returns comprehensive drug interaction medical inforamation for two given drugs or None",
    output_schema=pydantic_to_mcp_schema(DrugInteraction),
)
def wxobc_get_drug_interactions_tool(drug_name_1: str, drug_name_2: str) -> Optional[DrugInteraction]:
    """
    Retrieves information about interactions between two drugs

    This function fetches comprehensive drug interaction medical inforamation

    Args:
        drug_name_1 (str): The unique name of the drug 1
        drug_name_2 (str): The unique name of the drug 2

    Returns:
        Optional[DrugInteraction]: If an interaction is found
    """
    interaction: Optional[DrugInteraction] = DRUG_INTERACTIONS.get(f"{drug_name_1.lower()}_{drug_name_2.lower()}")
    if not interaction:
        interaction = DRUG_INTERACTIONS.get(f"{drug_name_2.lower()}_{drug_name_1.lower()}")
    return interaction


@mcp.tool(
    name="wxoGetDrugContraindications",
    description="Returns comprehensive drug contraindication medical inforamation for a given drug or None",
    output_schema=pydantic_to_mcp_schema(ContraindicationRule),
)
def wxobc_get_drug_contrindications_from_drug_name_tool(
    drug_name: str,
) -> Optional[ContraindicationRule]:
    """
    Retrieves information about contraindications for a drug

    This function fetches comprehensive drug contraindication medical inforamation

    Args:
        drug_name (str): The unique name of the drug

    Returns:
        Optional[ContraindicationRule]: if contraindications exist for the drug
    """
    contraindication: Optional[ContraindicationRule] = CONTRAINDICATION_RULES.get(drug_name.lower())
    return contraindication


@mcp.tool(
    name="wxoGetDrugAlternativeTreatments",
    description="Retrieves information about alternative treatments for a given drug or None",
    output_schema=pydantic_to_mcp_schema(AlternativeTreatment),
)
def wxobc_get_alternative_treatment_from_drug_name_tool(
    drug_name: str,
) -> AlternativeTreatment | None:
    """
    Retrieves information about alternative treatments for a drug

    This function fetches comprehensive alternative treatment medical inforamation

    Args:
        drug_name (str): The unique name of the drug

    Returns:
        Optional[AlternativeTreatment]: if alternative treatments exist for a drug
    """

    alt_treatment: Optional[AlternativeTreatment] = ALTERNATIVE_TREATMENTS.get(drug_name.lower())
    return alt_treatment


@mcp.tool(
    name="wxoGetPatient360",
    description="Given a patient id, construct a 360 view of a patient, their information, medical data and most recent vital signs",
    output_schema=pydantic_to_mcp_schema(Patient360),
)
def wxobc_create_patient_360_tool(patient_id: str) -> Patient360:
    pat: Optional[Patient] = SAMPLE_PATIENTS.get(patient_id)
    med: Optional[MedicalServerOutput] = SAMPLE_MEDICAL_SERVER.get(patient_id)
    vital: Optional[VitalSigns] = SAMPLE_BED_SIDE_DATA_SERVER.get(patient_id)
    if pat and vital:
        vital.estimate_creatinine_clearance(age=pat.age, sex=pat.sex)
    return Patient360(
        information=pat,
        medical=med,
        vital_signs=vital,
    )


# Your existing imports and functions...

logger = logging.getLogger(__name__)


async def main_async(sse_or_stdio: str):
    """Run the MCP server with comprehensive error handling"""
    global patient_dict, visit_dict, transcripts, device_stock_levels, drug_stock_levels, device_suppliers, drug_data, drug_suppliers

    try:
        logger.info("Starting MCP server...")
        # Add some debug info about the mcp module
        logger.info(f"Using MCP version: {getattr(mcp, '__version__', 'unknown')}")
        #################################################
        #
        # SSE
        #
        #################################################
        if sse_or_stdio == "SSE":
            print("(SSE) Data loaded successfully. Starting server on 0.0.0.0:8080...")
            # Run with SSE transport
            await mcp.run_async(transport="sse", host="0.0.0.0", port=8080)

        #################################################
        #
        # STDIO
        #
        #################################################
        if sse_or_stdio == "STDIO":
            print("(STDIO) Data loaded successfully. Starting server on STDIO")
            await mcp.run_async(transport="stdio")

    except Exception as e:
        logger.error(f"Error in main_async: {e}")
        import traceback

        traceback.print_exc()
        raise


# Keep this for backward compatibility if needed
def main():
    """Synchronous wrapper for the async main function"""
    asyncio.run(main_async("SSE"))


if __name__ == "__main__":
    main()
