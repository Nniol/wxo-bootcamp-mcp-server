from typing import Dict

from wxo_bootcamp_enum_constants import InteractionSeverity, Gender

from models.wxo_bootcamp_models import (
    Patient,
    PregnancyCategory,
    Prescription,
    Condition,
    VitalSigns,
    RiskLevel,
    Allergy,
    DrugInformation,
    AlternativeDrug,
    AlternativeTreatment,
    DrugInteraction,
    ContraindicationRule,
    MedicalServerOutput,
)


# =============================================================================
# SAMPLE DATA USING DICTIONARY STRUCTURES
# =============================================================================

# Sample conditions with ICD-10 codes for realistic API testing
SAMPLE_CONDITIONS: Dict[str, Condition] = {
    "COND001": Condition(
        condition_id="COND001",
        name="Atrial Fibrillation",
        short_name="atrial_fibrillation",
        icd10_code="I48.9",
        severity=RiskLevel.MODERATE,
        chronic=True,
    ),
    "COND002": Condition(
        condition_id="COND002",
        name="Essential Hypertension",
        short_name="essential_hypertension",
        icd10_code="I10",
        severity=RiskLevel.MODERATE,
        chronic=True,
    ),
    "COND003": Condition(
        condition_id="COND003",
        name="Type 2 Diabetes Mellitus",
        short_name="type_2_diabetes",
        icd10_code="E11.9",
        severity=RiskLevel.MODERATE,
        chronic=True,
    ),
    "COND004": Condition(
        condition_id="COND004",
        name="Chronic Kidney Disease Stage 3",
        short_name="chronic_kidney_disease",
        icd10_code="N18.3",
        severity=RiskLevel.HIGH,
        chronic=True,
    ),
    "COND005": Condition(
        condition_id="COND005",
        name="Major Depressive Disorder",
        short_name="major_depression",
        icd10_code="F32.9",
        severity=RiskLevel.MODERATE,
        chronic=True,
    ),
    "COND006": Condition(
        condition_id="COND006",
        name="Migraine",
        short_name="migraine",
        icd10_code="G43.9",
        severity=RiskLevel.LOW,
        chronic=True,
    ),
    "COND007": Condition(
        condition_id="COND007",
        name="Attention Deficit Hyperactivity Disorder",
        short_name="adhd",
        icd10_code="F90.9",
        severity=RiskLevel.LOW,
        chronic=True,
    ),
    "COND008": Condition(
        condition_id="COND008",
        name="Breast Cancer",
        short_name="breast_cancer",
        icd10_code="C50.9",
        severity=RiskLevel.HIGH,
        chronic=False,
    ),
    "COND009": Condition(
        condition_id="COND009",
        name="Cerebrovascular Accident",
        short_name="cerebrovascular_accident",
        icd10_code="I63.9",
        severity=RiskLevel.HIGH,
        chronic=False,
    ),
    "COND010": Condition(
        condition_id="COND010",
        name="Deep Vein Thrombosis",
        short_name="deep_vein_thrombosis",
        icd10_code="I82.40",
        severity=RiskLevel.HIGH,
        chronic=False,
    ),
    "COND011": Condition(
        condition_id="COND011",
        name="Epilepsy",
        short_name="epilepsy",
        icd10_code="G40.9",
        severity=RiskLevel.HIGH,
        chronic=True,
    ),
    "COND012": Condition(
        condition_id="COND012",
        name="Heart Failure",
        short_name="heart_failure",
        icd10_code="I50.9",
        severity=RiskLevel.HIGH,
        chronic=True,
    ),
    "COND013": Condition(
        condition_id="COND013",
        name="Osteoporosis",
        short_name="osteoporosis",
        icd10_code="M81.0",
        severity=RiskLevel.MODERATE,
        chronic=True,
    ),
    "COND014": Condition(
        condition_id="COND014",
        name="Generalized Anxiety Disorder",
        short_name="anxiety_disorder",
        icd10_code="F41.1",
        severity=RiskLevel.MODERATE,
        chronic=True,
    ),
    "COND015": Condition(
        condition_id="COND015",
        name="Bipolar Disorder",
        short_name="bipolar_disorder",
        icd10_code="F31.9",
        severity=RiskLevel.HIGH,
        chronic=True,
    ),
}

SAMPLE_ALLERGIES: Dict[str, Allergy] = {
    "penicillin": Allergy(
        allergen="penicillin", severity=RiskLevel.HIGH, reaction_type="anaphylaxis"
    ),
    "sulfonamides": Allergy(
        allergen="sulfonamides", severity=RiskLevel.MODERATE, reaction_type="skin rash"
    ),
    "ibuprofen": Allergy(
        allergen="ibuprofen",
        severity=RiskLevel.MODERATE,
        reaction_type="gastrointestinal bleeding",
    ),
    "codeine": Allergy(
        allergen="codeine",
        severity=RiskLevel.MODERATE,
        reaction_type="nausea and vomiting",
    ),
    "latex": Allergy(
        allergen="latex",
        severity=RiskLevel.MODERATE,
        reaction_type="contact dermatitis",
    ),
    "shellfish": Allergy(
        allergen="shellfish", severity=RiskLevel.HIGH, reaction_type="anaphylaxis"
    ),
}

# Sample patients designed to test various scenarios
SAMPLE_PATIENTS: Dict[str, Patient] = {
    "PAT001": Patient(  # elderly_high_risk
        patient_id="PAT001",
        age=78,
        sex=Gender.FEMALE,
        insurance_id="INS001ANON",
    ),
    "PAT002": Patient(  # pregnant_patient
        patient_id="PAT002",
        age=28,
        sex=Gender.FEMALE,
        pregnant=True,
        pregnancy_trimester=2,
        insurance_id="INS002ANON",
    ),
    "PAT003": Patient(  # young_adult_adhd
        patient_id="PAT003",
        age=22,
        sex=Gender.MALE,
        insurance_id="INS003ANON",
    ),
    "PAT004": Patient(  # middle_aged_depression
        patient_id="PAT004",
        age=45,
        sex=Gender.FEMALE,
        insurance_id="INS004ANON",
    ),
    "PAT005": Patient(  # elderly_diabetes
        patient_id="PAT005",
        age=72,
        sex=Gender.MALE,
        insurance_id="INS005ANON",
    ),
    "PAT006": Patient(  # cancer_patient
        patient_id="PAT006",
        age=55,
        sex=Gender.FEMALE,
        insurance_id="INS006ANON",
    ),
    "PAT007": Patient(  # pediatric_epilepsy
        patient_id="PAT007",
        age=12,
        sex=Gender.MALE,
        insurance_id="INS007ANON",
    ),
}

SAMPLE_BED_SIDE_DATA_SERVER: Dict[str, VitalSigns] = {
    "PAT001": VitalSigns(
        blood_pressure_systolic=165,
        blood_pressure_diastolic=95,
        heart_rate=88,
        weight_kg=68.0,
        height_cm=160.0,
        creatinine_mg_dl=1.8,
    ),
    "PAT002": VitalSigns(
        blood_pressure_systolic=145,
        blood_pressure_diastolic=90,
        heart_rate=82,
        weight_kg=75.0,
        height_cm=165.0,
        creatinine_mg_dl=0.8,
    ),
    "PAT003": VitalSigns(
        blood_pressure_systolic=125,
        blood_pressure_diastolic=80,
        heart_rate=75,
        weight_kg=70.0,
        height_cm=175.0,
        creatinine_mg_dl=1.0,
    ),
    "PAT004": VitalSigns(
        blood_pressure_systolic=135,
        blood_pressure_diastolic=85,
        heart_rate=70,
        weight_kg=80.0,
        height_cm=168.0,
        creatinine_mg_dl=1.1,
    ),
    "PAT005": VitalSigns(
        blood_pressure_systolic=150,
        blood_pressure_diastolic=88,
        heart_rate=65,
        weight_kg=85.0,
        height_cm=172.0,
        creatinine_mg_dl=1.6,
    ),
    "PAT006": VitalSigns(
        blood_pressure_systolic=140,
        blood_pressure_diastolic=85,
        heart_rate=78,
        weight_kg=62.0,
        height_cm=163.0,
        creatinine_mg_dl=1.2,
    ),
    "PAT007": VitalSigns(
        blood_pressure_systolic=105,
        blood_pressure_diastolic=70,
        heart_rate=85,
        weight_kg=45.0,
        height_cm=150.0,
        creatinine_mg_dl=0.6,
    ),
}

SAMPLE_MEDICAL_SERVER: Dict[str, MedicalServerOutput] = {
    "PAT001": MedicalServerOutput(
        conditions=[
            "atrial_fibrillation",  #: SAMPLE_CONDITIONS["COND001"],
            "essential_hypertension",  #: SAMPLE_CONDITIONS["COND002"],
            "chronic_kidney_disease",  #: SAMPLE_CONDITIONS["COND004"],
        ],
        allergies=["penicillin"],  # {"penicillin": SAMPLE_ALLERGIES["penicillin"]},
        prescriptions=[
            Prescription(
                prescription_id="RX001",
                drug_name="warfarin",
                brand_name="Coumadin",
                dose="5mg",
                frequency="once daily",
                indication="Atrial fibrillation anticoagulation",
            ),
            Prescription(
                prescription_id="RX002",
                drug_name="ibuprofen",
                brand_name="Advil",
                dose="600mg",
                frequency="three times daily",
                indication="Arthritis pain",
            ),
        ],
    ),
    "PAT002": MedicalServerOutput(
        conditions=[
            "essential_hypertension",
            "major_depression",
        ],  # SAMPLE_CONDITIONS["COND002"],SAMPLE_CONDITIONS["COND005"]
        prescriptions=[
            Prescription(
                prescription_id="RX003",
                drug_name="lisinopril",
                brand_name="Prinivil",
                dose="10mg",
                frequency="once daily",
                indication="Hypertension",
            )
        ],
    ),
    "PAT003": MedicalServerOutput(
        conditions=[
            "adhd",
            "anxiety_disorder",
        ],  # SAMPLE_CONDITIONS["COND007"], SAMPLE_CONDITIONS["COND014"],
        prescriptions=[
            Prescription(
                prescription_id="RX006",
                drug_name="methylphenidate",
                brand_name="Ritalin",
                dose="20mg",
                frequency="twice daily",
                indication="ADHD",
            ),
            Prescription(
                prescription_id="RX007",
                drug_name="alprazolam",
                brand_name="Xanax",
                dose="0.5mg",
                frequency="as needed",
                indication="Anxiety",
            ),
        ],
    ),
    "PAT004": MedicalServerOutput(
        conditions=[
            "major_depression",
            "migraine",
        ],  #  SAMPLE_CONDITIONS["COND005"], SAMPLE_CONDITIONS["COND006"]
        allergies=["ibuprofen"],  #: SAMPLE_ALLERGIES["ibuprofen"]],
        prescriptions=[
            Prescription(
                prescription_id="RX004",
                drug_name="sertraline",
                brand_name="Zoloft",
                dose="50mg",
                frequency="once daily",
                indication="Depression",
            ),
            Prescription(
                prescription_id="RX005",
                drug_name="tramadol",
                brand_name="Ultram",
                dose="50mg",
                frequency="every 6 hours",
                indication="Chronic pain",
            ),
        ],
    ),
    "PAT005": MedicalServerOutput(
        conditions=[
            "heart_failure",
            "type_2_diabetes",
            "essential_hypertension",
        ],  # SAMPLE_CONDITIONS["COND012"],SAMPLE_CONDITIONS["COND003"],SAMPLE_CONDITIONS["COND002"]
        prescriptions=[
            Prescription(
                prescription_id="RX008",
                drug_name="metformin",
                brand_name="Glucophage",
                dose="1000mg",
                frequency="twice daily",
                indication="Type 2 diabetes",
            ),
            Prescription(
                prescription_id="RX009",
                drug_name="enalapril",
                brand_name="Vasotec",
                dose="10mg",
                frequency="twice daily",
                indication="Heart failure",
            ),
            Prescription(
                prescription_id="RX010",
                drug_name="digoxin",
                brand_name="Lanoxin",
                dose="0.25mg",
                frequency="once daily",
                indication="Heart failure",
            ),
        ],
    ),
    "PAT006": MedicalServerOutput(
        conditions=[
            "breast_cancer",
            "major_depression",
            "deep_vein_thrombosis",
        ],  # SAMPLE_CONDITIONS["COND008"],SAMPLE_CONDITIONS["COND005"],SAMPLE_CONDITIONS["COND010"],
        prescriptions=[
            Prescription(
                prescription_id="RX011",
                drug_name="rivaroxaban",
                brand_name="Xarelto",
                dose="20mg",
                frequency="once daily",
                indication="DVT treatment",
            ),
            Prescription(
                prescription_id="RX012",
                drug_name="fluoxetine",
                brand_name="Prozac",
                dose="20mg",
                frequency="once daily",
                indication="Depression",
            ),
        ],
    ),
    "PAT007": MedicalServerOutput(
        conditions=["epilepsy"],  # SAMPLE_CONDITIONS["COND011"]},
        prescriptions=[
            Prescription(
                prescription_id="RX013",
                drug_name="phenytoin",
                brand_name="Dilantin",
                dose="100mg",
                frequency="twice daily",
                indication="Epilepsy control",
            )
        ],
    ),
}


# =============================================================================
# DRUG DATABASE AND INTERACTION PATTERNS
# =============================================================================

# Sample drug database using dictionaries
DRUG_DATABASE: Dict[str, DrugInformation] = {
    "warfarin": DrugInformation(
        drug_name="warfarin",
        brand_names=["Coumadin", "Jantoven"],
        drug_class="Anticoagulant",
        mechanism="Vitamin K antagonist",
        pregnancy_category=PregnancyCategory.X,
        controlled_substance=False,
        contraindications=["Active bleeding", "Pregnancy", "Severe liver disease"],
        warnings=["Major hemorrhage risk", "Regular INR monitoring required"],
        source_apis=["openfda", "rxnorm"],
    ),
    "rivaroxaban": DrugInformation(
        drug_name="rivaroxaban",
        brand_names=["Xarelto"],
        drug_class="Anticoagulant",
        mechanism="Factor Xa inhibitor",
        pregnancy_category=PregnancyCategory.C,
        controlled_substance=False,
        contraindications=["Active bleeding", "Severe renal impairment"],
        warnings=["Bleeding risk", "Avoid with strong CYP3A4 inhibitors"],
        source_apis=["openfda", "rxnorm"],
    ),
    "lisinopril": DrugInformation(
        drug_name="lisinopril",
        brand_names=["Prinivil", "Zestril"],
        drug_class="ACE Inhibitor",
        mechanism="Angiotensin converting enzyme inhibitor",
        pregnancy_category=PregnancyCategory.D,
        controlled_substance=False,
        contraindications=[
            "Pregnancy",
            "Angioedema history",
            "Bilateral renal artery stenosis",
        ],
        warnings=["Hyperkalemia", "Angioedema", "Kidney function decline"],
        source_apis=["openfda", "rxnorm"],
    ),
    "sertraline": DrugInformation(
        drug_name="sertraline",
        brand_names=["Zoloft"],
        drug_class="SSRI Antidepressant",
        mechanism="Selective serotonin reuptake inhibitor",
        pregnancy_category=PregnancyCategory.C,
        controlled_substance=False,
        contraindications=["MAOI use within 14 days", "Pimozide use"],
        warnings=["Serotonin syndrome", "Suicidal thoughts", "Bleeding risk"],
        source_apis=["openfda", "rxnorm"],
    ),
    "tramadol": DrugInformation(
        drug_name="tramadol",
        brand_names=["Ultram"],
        drug_class="Opioid Analgesic",
        mechanism="Mu-opioid receptor agonist, SNRI",
        pregnancy_category=PregnancyCategory.C,
        controlled_substance=True,
        contraindications=["Respiratory depression", "Acute intoxication"],
        warnings=["Serotonin syndrome", "Seizure risk", "Respiratory depression"],
        source_apis=["openfda", "rxnorm"],
    ),
    "ibuprofen": DrugInformation(
        drug_name="ibuprofen",
        brand_names=["Advil", "Motrin"],
        drug_class="NSAID",
        mechanism="COX-1 and COX-2 inhibitor",
        pregnancy_category=PregnancyCategory.C,
        controlled_substance=False,
        contraindications=["Active GI bleeding", "Severe heart failure"],
        warnings=["GI bleeding", "Cardiovascular events", "Kidney damage"],
        source_apis=["openfda", "rxnorm"],
    ),
    "methylphenidate": DrugInformation(
        drug_name="methylphenidate",
        brand_names=["Ritalin", "Concerta"],
        drug_class="CNS Stimulant",
        mechanism="Dopamine and norepinephrine reuptake inhibitor",
        pregnancy_category=PregnancyCategory.C,
        controlled_substance=True,
        contraindications=["Marked anxiety", "Glaucoma", "Motor tics"],
        warnings=[
            "Cardiovascular effects",
            "Growth suppression",
            "Psychiatric effects",
        ],
        source_apis=["openfda", "rxnorm"],
    ),
    "alprazolam": DrugInformation(
        drug_name="alprazolam",
        brand_names=["Xanax"],
        drug_class="Benzodiazepine",
        mechanism="GABA-A receptor enhancer",
        pregnancy_category=PregnancyCategory.D,
        controlled_substance=True,
        contraindications=[
            "Acute narrow-angle glaucoma",
            "Severe respiratory insufficiency",
        ],
        warnings=["Dependence", "Withdrawal", "CNS depression"],
        source_apis=["openfda", "rxnorm"],
    ),
}

# Critical drug interactions using dictionaries
DRUG_INTERACTIONS: Dict[str, DrugInteraction] = {
    "warfarin_tramadol": DrugInteraction(
        interaction_id="INT001",
        drug1="warfarin",
        drug2="tramadol",
        severity=InteractionSeverity.MAJOR,
        mechanism="Enhanced anticoagulation",
        clinical_effect="Increased bleeding risk",
        management="Monitor INR closely, consider dose reduction",
    ),
    "warfarin_ibuprofen": DrugInteraction(
        interaction_id="INT002",
        drug1="warfarin",
        drug2="ibuprofen",
        severity=InteractionSeverity.CONTRAINDICATED,
        mechanism="Antiplatelet effect + anticoagulation",
        clinical_effect="Severe bleeding risk",
        management="Avoid combination, use alternative analgesic",
    ),
    "sertraline_tramadol": DrugInteraction(
        interaction_id="INT003",
        drug1="sertraline",
        drug2="tramadol",
        severity=InteractionSeverity.MAJOR,
        mechanism="Dual serotonin enhancement",
        clinical_effect="Serotonin syndrome risk",
        management="Monitor for serotonin syndrome symptoms, avoid if possible",
    ),
    "methylphenidate_alprazolam": DrugInteraction(
        interaction_id="INT004",
        drug1="methylphenidate",
        drug2="alprazolam",
        severity=InteractionSeverity.MODERATE,
        mechanism="Opposing CNS effects",
        clinical_effect="Reduced effectiveness of both drugs",
        management="Monitor therapeutic response, adjust dosing if needed",
    ),
    "rivaroxaban_sertraline": DrugInteraction(
        interaction_id="INT005",
        drug1="rivaroxaban",
        drug2="sertraline",
        severity=InteractionSeverity.MODERATE,
        mechanism="Increased bleeding risk",
        clinical_effect="Enhanced anticoagulant effect",
        management="Monitor for bleeding signs, patient education",
    ),
}

CONTRAINDICATION_RULES: Dict[str, ContraindicationRule] = {
    "warfarin": ContraindicationRule(
        rule_id="CONTRA001",
        drug="warfarin",
        condition="pregnancy",
        severity=RiskLevel.CRITICAL,
        reason="Teratogenic - causes fetal warfarin syndrome",
    ),
    "lisinopril": ContraindicationRule(
        rule_id="CONTRA002",
        drug="lisinopril",
        condition="pregnancy",
        severity=RiskLevel.HIGH,
        reason="Can cause fetal kidney defects and oligohydramnios",
    ),
    "alprazolam": ContraindicationRule(
        rule_id="CONTRA003",
        drug="alprazolam",
        condition="elderly",
        severity=RiskLevel.HIGH,
        reason="Increased fall risk and cognitive impairment",
    ),
    "ibuprofen": ContraindicationRule(
        rule_id="CONTRA004",
        drug="ibuprofen",
        condition="chronic_kidney_disease",
        severity=RiskLevel.HIGH,
        reason="Can worsen kidney function",
    ),
    "tramadol": ContraindicationRule(
        rule_id="CONTRA005",
        drug="tramadol",
        condition="respiratory_depression",
        severity=RiskLevel.CRITICAL,
        reason="Life-threatening respiratory suppression",
    ),
}

ALTERNATIVE_TREATMENTS: Dict[str, AlternativeTreatment] = {
    "warfarin": AlternativeTreatment(
        original_drug="warfarin",
        alternatives={
            "rivaroxaban": AlternativeDrug(
                rationale="Direct oral anticoagulant with better safety profile",
                safety_improvement="No need for routine monitoring, lower bleeding risk",
                efficacy_comparison="Non-inferior for stroke prevention",
            ),
            "apixaban": AlternativeDrug(
                rationale="Lower bleeding risk than warfarin",
                safety_improvement="Reduced major bleeding, especially intracranial",
                efficacy_comparison="Superior efficacy for stroke prevention",
            ),
        },
        conditions=["pregnancy", "elderly_fall_risk", "poor_inr_control"],
    ),
    "ibuprofen": AlternativeTreatment(
        original_drug="ibuprofen",
        alternatives={
            "acetaminophen": AlternativeDrug(
                rationale="Safer for kidney function and bleeding risk",
                safety_improvement="No antiplatelet effect, kidney-safe",
                efficacy_comparison="Equal analgesic effect for mild-moderate pain",
            ),
            "topical_nsaid": AlternativeDrug(
                rationale="Localized effect with minimal systemic absorption",
                safety_improvement="Reduced GI and cardiovascular risks",
                efficacy_comparison="Effective for localized musculoskeletal pain",
            ),
        },
        conditions=[
            "kidney_disease",
            "anticoagulant_use",
            "elderly",
            "gi_bleeding_history",
        ],
    ),
    "lisinopril": AlternativeTreatment(
        original_drug="lisinopril",
        alternatives={
            "methyldopa": AlternativeDrug(
                rationale="First-line antihypertensive in pregnancy",
                safety_improvement="Pregnancy category B, well-studied safety profile",
                efficacy_comparison="Effective for pregnancy-induced hypertension",
            ),
            "labetalol": AlternativeDrug(
                rationale="Safe beta-blocker for pregnancy",
                safety_improvement="No teratogenic effects",
                efficacy_comparison="Effective for hypertensive emergencies in pregnancy",
            ),
        },
        conditions=["pregnancy"],
    ),
    "alprazolam": AlternativeTreatment(
        original_drug="alprazolam",
        alternatives={
            "sertraline": AlternativeDrug(
                rationale="SSRI safer in elderly for anxiety",
                safety_improvement="Lower fall risk, no cognitive impairment",
                efficacy_comparison="Effective for generalized anxiety disorder",
            ),
            "buspirone": AlternativeDrug(
                rationale="Non-benzodiazepine anxiolytic",
                safety_improvement="No sedation or dependence risk",
                efficacy_comparison="Effective for chronic anxiety",
            ),
        },
        conditions=["elderly", "fall_risk", "cognitive_impairment"],
    ),
}
