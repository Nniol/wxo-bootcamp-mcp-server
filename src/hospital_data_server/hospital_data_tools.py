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

from .models.data_enginner_adv_models import (
    PatientData,
    VisitData,
    DeviceStockLevel,
    DeviceSupplier,
    DrugData,
    AllDeviceSuppliers,
    AllDrugSuppliers,
    DrugStockLevel,
    DrugSupplier,
    AllDeviceStockLevels,
    AllDrugStockLevels,
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
from .util.load_data import (
    load_patient_csv,
    load_transcripts_json,
    load_visit_csv,
    load_device_stocklevels_csv,
    load_drug_data_csv,
    load_device_suppliers_csv,
    load_drug_stocklevels_csv,
    load_drug_suppliers_csv,
)
from .wxo_bootcamp_enum_constants import Gender

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
#    filename="mcp_server.log",
)
log = logging.getLogger("MCPServer")
# log.setLevel(logging.DEBUG)

# PROJECT_ROOT = Path(__file__).resolve().parent

mcp = FastMCP("hospital-data-server")

patient_dict: Dict[int, PatientData] = {}
visit_dict: Dict[int, VisitData] = {}
transcripts: Dict[int, str] = {}
device_stock_levels: Dict[str, DeviceStockLevel] = {}
drug_stock_levels: Dict[str, DrugStockLevel] = {}
device_suppliers: Dict[int, DeviceSupplier] = {}
drug_data: Dict[str, DrugData] = {}
drug_suppliers: Dict[int, DrugSupplier] = {}


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
    log.info(patient_dict)
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

        return patient_data
    raise Exception("visit_id not found")


@mcp.tool(
    name="Get All Device Stock Levels Data",
    description="Returns the initial stock levels of all devices in the hosptial.",
    output_schema=pydantic_to_mcp_schema(AllDeviceStockLevels),
)
async def get_all_device_stock_levels(ctx: Context) -> AllDeviceStockLevels:
    """Get All Initial Device Stock Levels

    Returns:
        AllDeviceStockLevels: All the initial Device Stock Levels
    """
    global device_stock_levels
    return AllDeviceStockLevels(device_stock_levels=list(device_stock_levels.values()))


@mcp.tool(
    name="Get Device Stock Level",
    description="Returns the initial stock level of a device in the hosptial.",
    output_schema=pydantic_to_mcp_schema(DeviceStockLevel),
)
async def get_device_stock_level(device_name: str, ctx: Context) -> DeviceStockLevel:
    """Get Initial Device Stock Level ffor a device

    Args:
        device_name (str): The device name to get the initial stock level for

    Returns:
        DeviceStockLevel: The DeviceStockLevel object
    """
    global device_stock_levels
    if device_name.lower() in device_stock_levels:
        device_sl = device_stock_levels[device_name.lower()]

        return device_sl
    raise Exception("device_name not found")


@mcp.tool(
    name="Get Drug Data",
    description="Returns the data about a drug.",
    output_schema=pydantic_to_mcp_schema(DrugData),
)
async def get_drug_data(drug_name: str, ctx: Context) -> DrugData:
    """Get Data on a Drug

    Args:
        drug_name (str): The drug name to get data for

    Returns:
        DrugData: The DrugData object
    """
    global drug_data
    if drug_name.lower() in drug_data:
        drug_data_obj = drug_data[drug_name.lower()]

        return drug_data_obj
    raise Exception("drug_name not found")


@mcp.tool(
    name="Get Drug Supplier",
    description="Returns a  drug supplier for the given id.",
    output_schema=pydantic_to_mcp_schema(DrugSupplier),
)
async def get_drug_supplier(supplier_id: int, ctx: Context) -> DrugSupplier:
    """Get supplier data for the given id

    Args:
        supplier_id (int): The drug supplier id to get data for

    Returns:
        DrugSupplier: The DrugSupplier object
    """
    global drug_suppliers
    if supplier_id in drug_suppliers:
        drug_supplier_obj = drug_suppliers[supplier_id]

        return drug_supplier_obj
    raise Exception("supplier_id not found")


@mcp.tool(
    name="Get Device Supplier",
    description="Returns a  Device supplier for the given id.",
    output_schema=pydantic_to_mcp_schema(DeviceSupplier),
)
async def get_device_supplier(supplier_id: int, ctx: Context) -> DeviceSupplier:
    """Get supplier data for the given id

    Args:
        supplier_id (int): The device supplier id to get data for

    Returns:
        DeviceSupplier: The DeviceSupplier object
    """
    global device_suppliers
    if supplier_id in drug_suppliers:
        device_supplier_obj = device_suppliers[supplier_id]

        return device_supplier_obj
    raise Exception("supplier_id not found")


@mcp.tool(
    name="Get All Device Suppliers",
    description="Returns all  Device suppliers.",
    output_schema=pydantic_to_mcp_schema(AllDeviceSuppliers),
)
async def get_all_device_suppliers(ctx: Context) -> AllDeviceSuppliers:
    """All device suppliers

    Returns:
        AllDeviceSuppliers: A list of  DeviceSupplier objects
    """
    global device_suppliers
    return AllDeviceSuppliers(device_suppliers=list(device_suppliers.values()))


@mcp.tool(
    name="Get All Drug Suppliers",
    description="Returns all  Drug suppliers.",
    output_schema=pydantic_to_mcp_schema(AllDrugSuppliers),
)
async def get_all_drug_suppliers(ctx: Context) -> AllDrugSuppliers:
    """All device suppliers

    Returns:
        AllDeviceSuppliers: A list of  DeviceSupplier objects
    """
    global drug_suppliers
    return AllDrugSuppliers(drug_suppliers=list(drug_suppliers.values()))


@mcp.tool(
    name="Get All Drug Stock Levels Data",
    description="Returns the initial stock levels of all drugs in the hosptial.",
    output_schema=pydantic_to_mcp_schema(AllDrugStockLevels),
)
async def get_all_drug_stock_levels(ctx: Context) -> AllDrugStockLevels:
    """Get All Initial Drug Stock Levels

    Returns:
        AllDrugStockLevels: All the DrugStockLevel objects
    """
    global drug_stock_levels
    return AllDrugStockLevels(drug_stock_levels=list(drug_stock_levels.values()))


@mcp.tool(
    name="Get Drug Stock Level",
    description="Returns the initial stock levels of a drug in the hosptial.",
    output_schema=pydantic_to_mcp_schema(DrugStockLevel),
)
async def get_drug_stock_level(drug_name: str, ctx: Context) -> DrugStockLevel:
    """Get Initial Drug Stock Level ffor a drug

    Args:
        drug_name (str): The device name to get the initial stock level for

    Returns:
        DrugStockLevel: The DrugStockLevel object
    """
    global drug_stock_levels
    if drug_name.lower() in drug_stock_levels:
        drug_sl = drug_stock_levels[drug_name.lower()]

        return drug_sl
    raise Exception("device_name not found")


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
    name="(WXO) Get Vital Signs Information",
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
    name="(WXO) Get Patient Information",
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
    name="(WXO) Get Medical Information",
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
    name="(WXO) Get Drug Information",
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
    name="(WXO) Get Drug Interations",
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
    name="(WXO) Get Drug Contraindications",
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
    name="(WXO) Get Drug Alternative Treatments",
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
    name="(WXO) Get Patient360",
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
        logger.info("Loading patient data...")
        patient_dict = load_patient_csv()
        logger.info(f"Loaded {len(patient_dict)} patients")

        logger.info("Loading visit data...")
        visit_dict = load_visit_csv()
        logger.info(f"Loaded {len(visit_dict)} visits")

        logger.info("Loading transcript data...")
        transcripts = load_transcripts_json()
        logger.info(f"Loaded {len(transcripts)} transcripts")

        logger.info("Loading device stock levels data...")
        device_stock_levels = load_device_stocklevels_csv()
        logger.info(f"Loaded {len(device_stock_levels)} device stock levels")

        logger.info("Loading device supplier data...")
        device_suppliers = load_device_suppliers_csv()
        logger.info(f"Loaded {len(device_suppliers)} device suppliers")

        logger.info("Loading drug stock levels data...")
        drug_stock_levels = load_drug_stocklevels_csv()
        logger.info(f"Loaded {len(drug_stock_levels)} drug stock levels")

        logger.info("Loading drug data...")
        drug_data = load_drug_data_csv()
        logger.info(f"Loaded {len(drug_data)} drug data")

        logger.info("Loading drug suppliers data...")
        drug_suppliers = load_drug_suppliers_csv()
        logger.info(f"Loaded {len(drug_suppliers)} drug suppliers data")

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
    asyncio.run(main_async())


if __name__ == "__main__":
    main()
