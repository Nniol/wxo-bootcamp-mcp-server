import ast
import asyncio
import json
import logging

from typing import Dict, Optional

import pandas as pd

from fastmcp.server import Context
from fastmcp.server import FastMCP
# from mcp.types import SamplingMessage, TextContent

from data.wxo_bootcamp_data import (
    SAMPLE_BED_SIDE_DATA_SERVER,
    SAMPLE_MEDICAL_SERVER,
    SAMPLE_PATIENTS,
    DRUG_DATABASE,
    DRUG_INTERACTIONS,
    CONTRAINDICATION_RULES,
    ALTERNATIVE_TREATMENTS,
)

from models.data_endinner_adv_models import PatientData, VisitData
from models.wxo_bootcamp_models import (
    AlternativeTreatment,
    ContraindicationRule,
    Patient,
    DrugInformation,
    DrugInteraction,
    MedicalServerOutput,
    Patient360,
    VitalSigns,
)
from util.pydantic_to_mcp import pydantic_to_mcp_schema
from wxo_bootcamp_enum_constants import Gender

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filename="mcp_server.log",
)
log = logging.getLogger("MCPServer")
# log.setLevel(logging.DEBUG)
mcp = FastMCP("hospital-data-server")


patient_dict: Dict[int, PatientData] = {}
visit_dict: Dict[int, VisitData] = {}
transcripts: Dict[int, str] = {}


def load_patient_csv() -> Dict[int, PatientData]:
    log.info("Loading Patient Data")
    df = pd.read_csv("data/patients.csv")
    t_dict = df.to_dict("records")
    d_dict: Dict[int, PatientData] = {
        int(d["PatientID"]): PatientData(
            patient_id=int(d["PatientID"]),
            name=d["Name"],
            age=d["Age"],
            sex=d["Sex"],
            zip_code=d["zip_code"],
            personality=d["personality"],
        )
        for d in t_dict
    }
    log.info("Loaded Patient Data")
    return d_dict


def load_visit_csv() -> Dict[int, VisitData]:
    log.info("Loading Visit Data")
    df = pd.read_csv("data/visits.csv")
    t_dict = df.to_dict("records")
    d_dict: Dict[int, VisitData] = {
        int(d["VisitID"]): VisitData(
            visit_id=int(d["VisitID"]),
            patient_id=int(d["PatientID"]),
            date=d["VisitDate"],
            chief_complaint=d["ChiefComplaint"],
            tests=ast.literal_eval(d["Tests"]),
            diagnosis_from_test=d["DiagnosisFromTest"],
            diagnosis=d["Diagnosis"],
            treatment=d["Treatment"],
            medicines=ast.literal_eval(d["medicines"]),
            painkillers=ast.literal_eval(d["painkillers"]),
            antibiotics=ast.literal_eval(d["antibiotics"]),
            died=d["Died"],
        )
        for d in t_dict
    }
    log.info("Loaded Visit Data")
    return d_dict


def load_transcripts_json() -> Dict[int, str]:
    log.info("Loading Transcript Data")
    with open("data/1000_transcripts.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    log.info("Loaded Transcript Data")
    return data


@mcp.tool(
    name="Get Patient Data",
    description="Returns basic patient data (Name, Age, Sex etc.), or raise an Exception if not found.",
    output_schema=pydantic_to_mcp_schema(PatientData),
)
async def get_patient_data(patient_id: int, ctx: Context) -> PatientData:
    """Get Patient Data

    Args:
        patient_id (int): The Unique Identifier of the patient

    Returns:
        PatientData: PatientData Object
    """
    global patient_dict
    if patient_id in patient_dict:
        patient_data = patient_dict[patient_id]

        log.debug(patient_data.model_dump_json())
        return patient_data
    raise Exception("patient_id not found")


@mcp.tool(
    name="Get Visit Data",
    description="Returns the data describing the result of a visit to a hospital doctor, or raise an Exception if not found.",
    output_schema=pydantic_to_mcp_schema(VisitData),
)
async def get_visit_data(visit_id: int, ctx: Context) -> VisitData:
    """Get Visit Data

    Args:
        visit_id (int): The Unique Identifier of the visit

    Returns:
        VisitData: VisitData Object
    """
    global visit_dict
    if visit_id in visit_dict:
        patient_data = visit_dict[visit_id]

        log.debug(patient_data.model_dump_json())
        return patient_data
    raise Exception("visit_id not found")


@mcp.tool(
    name="Get Visit Transcript",
    description="Returns the transcript of a visit, or raise an Exception if not found.",
)
async def get_visit_transcript(visit_id: int, ctx: Context) -> str:
    """Get Transcript of the Vist

    Args:
        visit_id (int): The Unique Identifier of the visit,

    Returns:
        str: The transcript of the visit if one exists
    """
    global transcripts
    visit_id_str = str(visit_id)
    if visit_id_str in transcripts:
        transcript = transcripts[visit_id_str]
        log.debug(f"{visit_id}: {transcript[:100]}")
        return transcript
    raise Exception("visit_id not found")


@mcp.tool(
    name="Get Vital Signs Information",
    description="Returns patient vital signs from the bedside system (Blood pressure, pulse, creatine data, bmi, weight, height) or None.",
    output_schema=pydantic_to_mcp_schema(VitalSigns),
)
def wxobc_get_vital_signs_data_tool(
    patient_id: str, age: int, sex: str
) -> Optional[VitalSigns]:
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
    name="Get Patient Information",
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
    name="Get Medical Information",
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
    name="Get Drug Information",
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
    name="Get Drug Interations",
    description="Returns comprehensive drug interaction medical inforamation for two given drugs or None",
    output_schema=pydantic_to_mcp_schema(DrugInteraction),
)
def wxobc_get_drug_interactions_tool(
    drug_name_1: str, drug_name_2: str
) -> Optional[DrugInteraction]:
    """
    Retrieves information about interactions between two drugs

    This function fetches comprehensive drug interaction medical inforamation

    Args:
        drug_name_1 (str): The unique name of the drug 1
        drug_name_2 (str): The unique name of the drug 2

    Returns:
        Optional[DrugInteraction]: If an interaction is found
    """
    interaction: Optional[DrugInteraction] = DRUG_INTERACTIONS.get(
        f"{drug_name_1.lower()}_{drug_name_2.lower()}"
    )
    if not interaction:
        interaction = DRUG_INTERACTIONS.get(
            f"{drug_name_2.lower()}_{drug_name_1.lower()}"
        )
    return interaction


@mcp.tool(
    name="Get Drug Contraindications",
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
    contraindication: Optional[ContraindicationRule] = CONTRAINDICATION_RULES.get(
        drug_name.lower()
    )
    return contraindication


@mcp.tool(
    name="Get Drug Alternative Treatments",
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

    alt_treatment: Optional[AlternativeTreatment] = ALTERNATIVE_TREATMENTS.get(
        drug_name.lower()
    )
    return alt_treatment


@mcp.tool(
    name="Get Patient360",
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


async def main():
    global patient_dict, visit_dict, transcripts
    patient_dict = load_patient_csv()
    visit_dict = load_visit_csv()
    transcripts = load_transcripts_json()
    """Run the MCP server with SSE transport"""
    # Run with SSE transport on localhost:8000
    await mcp.run_async(transport="sse", host="localhost", port=8000)


# if __name__ == "__main__":
#     print("Starting MCP server with SSE transport on http://localhost:8000")
#     print("SSE endpoint: http://localhost:8000/sse")
#     print("Messages endpoint: http://localhost:8000/messages")

#     # Run the server
#     asyncio.run(main())
