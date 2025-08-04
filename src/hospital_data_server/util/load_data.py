import ast
import json
import logging

from importlib import resources
from pathlib import Path
from typing import Dict

import pandas as pd

from ..models.data_enginner_adv_models import PatientData, VisitData, DeviceStockLevel, DeviceSupplier, DrugData, DrugStockLevel, DrugSupplier

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filename="mcp_server.log",
)
log = logging.getLogger("MCPServer")


def load_device_stocklevels_csv() -> Dict[str, DeviceStockLevel]:
    log.info("Loading Device Stock Data")
    try:
        # Modern approach using files()
        data_files = resources.files("hospital_data_server.data")
        patients_file = data_files / "device_stock_levels.csv"
        with patients_file.open("r") as f:
            df = pd.read_csv(f)
    except (ImportError, FileNotFoundError, ModuleNotFoundError, AttributeError):
        # Fallback for development or older Python
        current_dir = Path(__file__).parent
        data_path = current_dir / "data" / "device_stock_levels.csv"
        if not data_path.exists():
            project_root = current_dir.parent.parent
            data_path = project_root / "data" / "device_stock_levels.csv"
        df = pd.read_csv(data_path)
    t_dict = df.to_dict("records")

    # Device Name,Initial Stock (Units),Reorder Level (Units)
    d_dict: Dict[str, DeviceStockLevel] = {
        d["Device Name"].lower(): DeviceStockLevel(device_name=d["Device Name"], initial_stock=d["Initial Stock (Units)"], re_order_level=d["Reorder Level (Units)"]) for d in t_dict
    }
    log.info("Loaded Device Stock Data")
    return d_dict


def load_device_suppliers_csv() -> Dict[int, DeviceSupplier]:
    log.info("Loading Device Supplier Data")
    try:
        # Modern approach using files()
        data_files = resources.files("hospital_data_server.data")
        patients_file = data_files / "device_suppliers.csv"
        with patients_file.open("r") as f:
            df = pd.read_csv(f)
    except (ImportError, FileNotFoundError, ModuleNotFoundError, AttributeError):
        # Fallback for development or older Python
        current_dir = Path(__file__).parent
        data_path = current_dir / "data" / "device_suppliers.csv"
        if not data_path.exists():
            project_root = current_dir.parent.parent
            data_path = project_root / "data" / "device_suppliers.csv"
        df = pd.read_csv(data_path)
    t_dict = df.to_dict("records")

    # Device Name,Initial Stock (Units),Reorder Level (Units)
    d_dict: Dict[int, DeviceSupplier] = {
        d["id"]: DeviceSupplier(
            id=d["id"],
            name=d["SupplierName"],
            specialization=d["Specialization"].split(","),
            address=d["Address"],
            phone=d["Phone"],
            email=d["Email"],
            lead_time=d["LeadTimeInDays"],
            reliablity=d["Reliability"],
        )
        for d in t_dict
    }
    log.info("Loaded Device Supplier Data")
    return d_dict


def load_drug_stocklevels_csv() -> Dict[str, DrugStockLevel]:
    log.info("Loading Drug Stock Data")
    try:
        # Modern approach using files()
        data_files = resources.files("hospital_data_server.data")
        patients_file = data_files / "drug_stock_levels.csv"
        with patients_file.open("r") as f:
            df = pd.read_csv(f)
    except (ImportError, FileNotFoundError, ModuleNotFoundError, AttributeError):
        # Fallback for development or older Python
        current_dir = Path(__file__).parent
        data_path = current_dir / "data" / "drug_stock_levels.csv"
        if not data_path.exists():
            project_root = current_dir.parent.parent
            data_path = project_root / "data" / "drug_stock_levels.csv"
        df = pd.read_csv(data_path)
    t_dict = df.to_dict("records")

    # Device Name,Initial Stock (Doses),Reorder Level (Doses)
    d_dict: Dict[str, DrugStockLevel] = {
        d["Drug Name"].lower(): DrugStockLevel(name=d["Drug Name"], initial_stock=d["Initial Stock (Doses)"], re_order_level=d["Reorder Level (Doses)"]) for d in t_dict
    }
    log.info("Loaded Drug Stock Data")
    return d_dict


def load_drug_data_csv() -> Dict[str, DrugData]:
    log.info("Loading Drug Data")
    try:
        # Modern approach using files()
        data_files = resources.files("hospital_data_server.data")
        patients_file = data_files / "drug_data.csv"
        with patients_file.open("r") as f:
            df = pd.read_csv(f)
    except (ImportError, FileNotFoundError, ModuleNotFoundError, AttributeError):
        # Fallback for development or older Python
        current_dir = Path(__file__).parent
        data_path = current_dir / "data" / "drug_data.csv"
        if not data_path.exists():
            project_root = current_dir.parent.parent
            data_path = project_root / "data" / "drug_data.csv"
        df = pd.read_csv(data_path)
    t_dict = df.to_dict("records")

    # Device Name,Initial Stock (Units),Reorder Level (Units)
    d_dict: Dict[str, DrugData] = {
        d["Drug Name"].lower(): DrugData(
            name=d["Drug Name"], cost=d["Cost Per Packet"], packet_size=d["Packet Size"], volume=d["Volume"], dose_volume=d["Dose Volume"], shelf_life=d["Shelf Life (Days)"]
        )
        for d in t_dict
    }
    log.info("Loaded Drug Data")
    return d_dict


def load_drug_suppliers_csv() -> Dict[int, DrugSupplier]:
    log.info("Loading Drug Supplier Data")
    try:
        # Modern approach using files()
        data_files = resources.files("hospital_data_server.data")
        patients_file = data_files / "drug_suppliers.csv"
        with patients_file.open("r") as f:
            df = pd.read_csv(f)
    except (ImportError, FileNotFoundError, ModuleNotFoundError, AttributeError):
        # Fallback for development or older Python
        current_dir = Path(__file__).parent
        data_path = current_dir / "data" / "drug_suppliers.csv"
        if not data_path.exists():
            project_root = current_dir.parent.parent
            data_path = project_root / "data" / "drug_suppliers.csv"
        df = pd.read_csv(data_path)
    t_dict = df.to_dict("records")

    # Device Name,Initial Stock (Units),Reorder Level (Units)
    d_dict: Dict[int, DrugSupplier] = {
        d["id"]: DrugSupplier(
            id=d["id"],
            name=d["SupplierName"],
            specialization=d["Specialization"].split(","),
            address=d["Address"],
            phone=d["Phone"],
            email=d["Email"],
            lead_time=d["LeadTimeInDays"],
            reliablity=d["Reliability"],
        )
        for d in t_dict
    }
    log.info("Loaded Drug Supplier Data")
    return d_dict


def load_patient_csv() -> Dict[int, PatientData]:
    log.info("Loading Patient Data")
    try:
        # Modern approach using files()
        data_files = resources.files("hospital_data_server.data")
        patients_file = data_files / "patients.csv"
        with patients_file.open("r") as f:
            df = pd.read_csv(f)
    except (ImportError, FileNotFoundError, ModuleNotFoundError, AttributeError):
        # Fallback for development or older Python
        current_dir = Path(__file__).parent
        data_path = current_dir / "data" / "patients.csv"
        if not data_path.exists():
            project_root = current_dir.parent.parent
            data_path = project_root / "data" / "patients.csv"
        df = pd.read_csv(data_path)
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
    try:
        data_files = resources.files("hospital_data_server.data")
        visits_file = data_files / "visits.csv"
        with visits_file.open("r") as f:
            df = pd.read_csv(f)
    except (ImportError, FileNotFoundError, ModuleNotFoundError, AttributeError):
        current_dir = Path(__file__).parent
        data_path = current_dir / "data" / "visits.csv"
        if not data_path.exists():
            project_root = current_dir.parent.parent
            data_path = project_root / "data" / "visits.csv"
        df = pd.read_csv(data_path)

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
    try:
        data_files = resources.files("hospital_data_server.data")
        transcripts_file = data_files / "1000_transcripts.json"
        with transcripts_file.open("r") as f:
            transcripts = json.load(f)
    except (ImportError, FileNotFoundError, ModuleNotFoundError, AttributeError):
        current_dir = Path(__file__).parent
        data_path = current_dir / "data" / "1000_transcripts.json"
        if not data_path.exists():
            project_root = current_dir.parent.parent
            data_path = project_root / "data" / "1000_transcripts.json"
        with open(data_path, "r") as f:
            transcripts = json.load(f)

    return transcripts
