from typing import List, Dict

TABLES_INFO = [
    {"table": "RPT_SUBJECT_DISPOSITION", "desc": "Subject enrollment, completion, withdrawal, death status"},
    {"table": "RPT_AE", "desc": "Adverse events with severity, seriousness, MedDRA coding"},
    {"table": "RPT_LAB_INFORMATION", "desc": "Laboratory test results and abnormal flags"},
    {"table": "RPT_EG", "desc": "Electrocardiogram (ECG) measurements and abnormalities"},
    {"table": "RPT_VS", "desc": "Vital signs (BP, HR, temp, weight, height)"},
    {"table": "RPTTAB_DV", "desc": "Protocol deviations and violations"},
    {"table": "RPT_RS", "desc": "Response assessment and tumor measurements"},
    {"table": "RPT_EX", "desc": "Drug exposure, dosage, frequency, duration"},
    {"table": "RPT_GRAPHICAL_PATIENT_PROFILE", "desc": "Integrated patient data across domains"},
    {"table": "RPT_SV", "desc": "Subject visit information and schedules"},
    {"table": "RPT_SUBJECT_DAYS", "desc": "Subject days on study by month"},
    {"table": "RPT_AE_SEV_GRADE", "desc": "Adverse events with toxicity grades"},
    {"table": "RPT_STUDY_DETAILS", "desc": "Study metadata and CRO details"},
    {"table": "RPT_SUBJECT_STORY", "desc": "Patient journey with events timeline"},
    {"table": "RPT_SUBJECT_DETAIL", "desc": "Demographics, BMI, height, weight, status"},
    {"table": "RPT_MH", "desc": "Medical history and ongoing conditions"},
    {"table": "RPT_TUMOR_DETAIL", "desc": "Tumor response assessment in oncology trials"}
]


def format_tables_for_llm() -> str:
    formatted = "Available Tables:\n"
    for i, t in enumerate(TABLES_INFO, 1):
        formatted += f"{i}. {t['table']}: {t['desc']}\n"
    return formatted
