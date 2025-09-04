from typing import List, Dict

from pydantic import BaseModel, Field


class DeviceStockLevel(BaseModel):
    # Device Name,Initial Stock (Units),Reorder Level (Units)
    device_name: str = Field(description="The name of the device")
    initial_stock: int = Field(description="The initial stock level of the hospital in units")
    re_order_level: int = Field(description="At what level should the stock be reordered")


class AllDeviceStockLevels(BaseModel):
    device_stock_levels: List[DeviceStockLevel] = Field(description="List of all the inital stock levels for devices in the hospital")


class DeviceSupplier(BaseModel):
    # id,SupplierName,Specialization,Address,Phone,Email,LeadTimeInDays,Reliability
    id: int = Field(description="Supplier ID")
    name: str = Field(description="Supplier name")
    specialization: List[str] = Field(description="Which devices are available from this supplier")
    address: str = Field(description="Supplier's Address")
    phone: str = Field(description="Supplier phone number")
    email: str = Field(description="Supplier email")
    lead_time: str = Field(description="Lead time for the supplier to deliver, measured in a span of days")
    reliablity: str = Field(description="How reliable is the supplier")


class AllDeviceSuppliers(BaseModel):
    device_suppliers: List[DeviceSupplier] = Field(description="List of all the device suppliers")


class DrugData(BaseModel):
    # Drug Name,Cost Per Packet,Packet Size,Volume,Dose Volume,Shelf Life (Days)
    name: str = Field(description="Drug Name")
    cost: float = Field(description="Cost per unit (package, bottle etc.)")
    packet_size: int = Field(description="Number of pills per packet, if the drug is in pill form")
    volume: int = Field(description="Volume of bottle if the drug is in liquid form")
    dose_volume: float = Field(description="Typical volume of one dose")
    shelf_life: int = Field(description="How long can the drug stay on the shelf before it needs replacing")


class DrugStockLevel(BaseModel):
    # Drug Name,Initial Stock (Doses),Reorder Level (Doses)
    name: str = Field(description="Drug Name")
    initial_stock: int = Field(description="The initial stock level of the hospital in doses")
    re_order_level: int = Field(description="At what level should the stock be reordered in doses")


class AllDrugStockLevels(BaseModel):
    drug_stock_levels: List[DrugStockLevel] = Field(description="List of all the inital stock levels for drugs in the hospital")


class DrugSupplier(BaseModel):
    # id, Supplier Name,Specialization,Address,Phone,Email,Lead Time (Days),Reliability
    id: int = Field(description="Supplier ID")
    name: str = Field(description="Supplier name")
    specialization: List[str] = Field(description="Which drugs are available from this supplier")
    address: str = Field(description="Supplier's Address")
    phone: str = Field(description="Supplier phone number")
    email: str = Field(description="Supplier email")
    lead_time: str = Field(description="Lead time for the supplier to deliver, measured in a span of days")
    reliablity: str = Field(description="How reliable is the supplier")


class AllDrugSuppliers(BaseModel):
    drug_suppliers: List[DrugSupplier] = Field(description="List of all the drug suppliers")


class PatientData(BaseModel):
    patient_id: int = Field(description="The patient's unique identifier.")
    name: str = Field(description="The patient's name")
    age: int = Field(description="The patienbt's age")
    sex: str = Field(description="The patient's gender")
    zip_code: int = Field(description="The patient's zip code")
    personality: str = Field(description="The personality of the patient. Used when generating transcripts")


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
