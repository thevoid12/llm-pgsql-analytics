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

TABLE_COLUMNS = {
    "RPT_SUBJECT_DISPOSITION": {
        "description": "Subject enrollment, completion, withdrawal, death status",
        "columns": [
            {"name": "comprehendid", "type": "TEXT", "desc": "Unique identifier for the record"},
            {"name": "studyid", "type": "TEXT", "desc": "Study identifier"},
            {"name": "siteid", "type": "TEXT", "desc": "Site identifier"},
            {"name": "usubjid", "type": "TEXT", "desc": "Unique subject identifier"},
            {"name": "dsterm", "type": "TEXT", "desc": "Disposition event term (Completed, Withdrew Consent)"},
            {"name": "dsstdtc", "type": "DATE", "desc": "Start date of disposition event"},
            {"name": "dsdecod", "type": "TEXT", "desc": "Decoded disposition term"},
            {"name": "visit", "type": "TEXT", "desc": "Visit name"},
            {"name": "visitnum", "type": "NUMERIC", "desc": "Visit number"},
            {"name": "studyname", "type": "TEXT", "desc": "Study name"},
            {"name": "sitename", "type": "TEXT", "desc": "Site name"},
            {"name": "sitecountry", "type": "TEXT", "desc": "Site country"},
            {"name": "siteregion", "type": "TEXT", "desc": "Site region (Americas, Europe, Asia)"},
            {"name": "dswithdrawn", "type": "BOOLEAN", "desc": "Indicates withdrawal"},
            {"name": "dscompleted", "type": "BOOLEAN", "desc": "Indicates completion"},
            {"name": "deathcause", "type": "TEXT", "desc": "Cause of death"},
            {"name": "deathdate", "type": "DATE", "desc": "Date of death"},
            {"name": "arm", "type": "TEXT", "desc": "Treatment arm"},
        ]
    },
    "RPT_AE": {
        "description": "Adverse events with severity, seriousness, MedDRA coding",
        "columns": [
            {"name": "comprehendid", "type": "TEXT", "desc": "Unique identifier"},
            {"name": "studyid", "type": "TEXT", "desc": "Study identifier"},
            {"name": "siteid", "type": "TEXT", "desc": "Site identifier"},
            {"name": "usubjid", "type": "TEXT", "desc": "Unique subject identifier"},
            {"name": "aeterm", "type": "TEXT", "desc": "Adverse event term"},
            {"name": "aebodsys", "type": "TEXT", "desc": "Body system affected"},
            {"name": "aestdtc", "type": "DATE", "desc": "AE start date"},
            {"name": "aeendtc", "type": "DATE", "desc": "AE end date"},
            {"name": "aesev", "type": "TEXT", "desc": "Severity (Mild, Moderate, Severe)"},
            {"name": "aeser", "type": "TEXT", "desc": "Seriousness (Serious, Non-Serious)"},
            {"name": "aerelnst", "type": "TEXT", "desc": "Relationship to study intervention"},
            {"name": "preferredterm", "type": "TEXT", "desc": "MedDRA Preferred Term"},
            {"name": "aesoc", "type": "TEXT", "desc": "System Organ Class (MedDRA)"},
            {"name": "aeout", "type": "TEXT", "desc": "Outcome of AE"},
            {"name": "aetoxgr", "type": "TEXT", "desc": "Toxicity grade"},
            {"name": "aeongo", "type": "TEXT", "desc": "Is AE ongoing (Yes/No)"},
            {"name": "studyname", "type": "TEXT", "desc": "Study name"},
            {"name": "sitename", "type": "TEXT", "desc": "Site name"},
            {"name": "sitecountry", "type": "TEXT", "desc": "Site country"},
            {"name": "siteregion", "type": "TEXT", "desc": "Site region"},
            {"name": "arm", "type": "TEXT", "desc": "Treatment arm"},
            {"name": "age", "type": "NUMERIC", "desc": "Subject age"},
            {"name": "sex", "type": "TEXT", "desc": "Subject sex"},
            {"name": "race", "type": "TEXT", "desc": "Subject race"},
            {"name": "visit", "type": "TEXT", "desc": "Visit name"},
            {"name": "visitnum", "type": "NUMERIC", "desc": "Visit number"},
        ]
    },
    "RPT_LAB_INFORMATION": {
        "description": "Laboratory test results and abnormal flags",
        "columns": [
            {"name": "comprehendid", "type": "TEXT", "desc": "Unique identifier"},
            {"name": "studyid", "type": "TEXT", "desc": "Study identifier"},
            {"name": "siteid", "type": "TEXT", "desc": "Site identifier"},
            {"name": "usubjid", "type": "TEXT", "desc": "Unique subject identifier"},
            {"name": "visit", "type": "TEXT", "desc": "Visit name"},
            {"name": "visitnum", "type": "NUMERIC", "desc": "Visit number"},
            {"name": "visitdy", "type": "INTEGER", "desc": "Study day of visit"},
            {"name": "arm", "type": "TEXT", "desc": "Treatment arm"},
            {"name": "lbdtc", "type": "TIMESTAMP", "desc": "Lab specimen collection date/time"},
            {"name": "lbtest", "type": "TEXT", "desc": "Lab test name (Calcium, Hemoglobin, Cholesterol)"},
            {"name": "lbtestcd", "type": "TEXT", "desc": "Lab test code"},
            {"name": "lbcat", "type": "TEXT", "desc": "Lab test category"},
            {"name": "lbstresn", "type": "NUMERIC", "desc": "Standardized numeric lab result"},
            {"name": "lbstresu", "type": "TEXT", "desc": "Standardized unit"},
            {"name": "lbnrind", "type": "TEXT", "desc": "Normal range indicator (Normal, High, Low)"},
            {"name": "lbstnrlo", "type": "NUMERIC", "desc": "Lower limit of normal range"},
            {"name": "lbstnrhi", "type": "NUMERIC", "desc": "Upper limit of normal range"},
            {"name": "issubjabnormal", "type": "BOOLEAN", "desc": "Subject had abnormal result for test"},
            {"name": "baseline_deviation", "type": "NUMERIC", "desc": "Percentage deviation from baseline"},
            {"name": "studyname", "type": "TEXT", "desc": "Study name"},
            {"name": "sitename", "type": "TEXT", "desc": "Site name"},
            {"name": "sitecountry", "type": "TEXT", "desc": "Site country"},
            {"name": "siteregion", "type": "TEXT", "desc": "Site region"},
        ]
    },
    "RPT_EG": {
        "description": "Electrocardiogram (ECG) measurements and abnormalities",
        "columns": [
            {"name": "comprehendid", "type": "TEXT", "desc": "Unique identifier"},
            {"name": "studyid", "type": "TEXT", "desc": "Study identifier"},
            {"name": "siteid", "type": "TEXT", "desc": "Site identifier"},
            {"name": "usubjid", "type": "TEXT", "desc": "Unique subject identifier"},
            {"name": "egtestcd", "type": "TEXT", "desc": "ECG test code (HR, QT, QTc)"},
            {"name": "egtest", "type": "TEXT", "desc": "ECG test name (Heart Rate, QT Interval)"},
            {"name": "egcat", "type": "TEXT", "desc": "ECG category"},
            {"name": "egstresn", "type": "NUMERIC", "desc": "Standardized numeric ECG result"},
            {"name": "egstresu", "type": "TEXT", "desc": "Standardized unit"},
            {"name": "visit", "type": "TEXT", "desc": "Visit name"},
            {"name": "visitdate", "type": "TIMESTAMP", "desc": "Visit date"},
            {"name": "egdtc", "type": "TIMESTAMP", "desc": "ECG date/time"},
            {"name": "isabnormal", "type": "BOOLEAN", "desc": "ECG result is abnormal"},
            {"name": "egclsig", "type": "TEXT", "desc": "Clinical significance"},
            {"name": "baseline_deviation", "type": "NUMERIC", "desc": "Percentage deviation from baseline"},
        ]
    },
    "RPT_VS": {
        "description": "Vital signs (BP, HR, temp, weight, height)",
        "columns": [
            {"name": "comprehendid", "type": "TEXT", "desc": "Unique identifier"},
            {"name": "studyid", "type": "TEXT", "desc": "Study identifier"},
            {"name": "siteid", "type": "TEXT", "desc": "Site identifier"},
            {"name": "usubjid", "type": "TEXT", "desc": "Unique subject identifier"},
            {"name": "vstestcd", "type": "TEXT", "desc": "Vital sign test code (TEMP, PULSE, SYSBP, DIABP, WEIGHT, HEIGHT)"},
            {"name": "vstest", "type": "TEXT", "desc": "Vital sign test name (Temperature, Pulse Rate, Blood Pressure)"},
            {"name": "vsstresn", "type": "NUMERIC", "desc": "Standardized numeric result"},
            {"name": "vsstresu", "type": "TEXT", "desc": "Standardized unit"},
            {"name": "visit", "type": "TEXT", "desc": "Visit name"},
            {"name": "visitnum", "type": "NUMERIC", "desc": "Visit number"},
            {"name": "vsdtc", "type": "TIMESTAMP", "desc": "Vital sign date/time"},
            {"name": "isabnormal", "type": "BOOLEAN", "desc": "Result is abnormal"},
            {"name": "baseline_deviation", "type": "NUMERIC", "desc": "Percentage deviation from baseline"},
            {"name": "arm", "type": "TEXT", "desc": "Treatment arm"},
        ]
    },
    "RPTTAB_DV": {
        "description": "Protocol deviations and violations",
        "columns": [
            {"name": "comprehendid", "type": "TEXT", "desc": "Unique identifier"},
            {"name": "studyid", "type": "TEXT", "desc": "Study identifier"},
            {"name": "siteid", "type": "TEXT", "desc": "Site identifier"},
            {"name": "usubjid", "type": "TEXT", "desc": "Unique subject identifier"},
            {"name": "dvterm", "type": "TEXT", "desc": "Deviation term"},
            {"name": "dvcat", "type": "TEXT", "desc": "Deviation category"},
            {"name": "dvstdtc", "type": "DATE", "desc": "Deviation start date"},
            {"name": "dvendtc", "type": "DATE", "desc": "Deviation end date"},
            {"name": "visit", "type": "TEXT", "desc": "Visit name"},
            {"name": "visitnum", "type": "NUMERIC", "desc": "Visit number"},
        ]
    },
    "RPT_EX": {
        "description": "Drug exposure, dosage, frequency, duration",
        "columns": [
            {"name": "comprehendid", "type": "TEXT", "desc": "Unique identifier"},
            {"name": "studyid", "type": "TEXT", "desc": "Study identifier"},
            {"name": "siteid", "type": "TEXT", "desc": "Site identifier"},
            {"name": "usubjid", "type": "TEXT", "desc": "Unique subject identifier"},
            {"name": "extrt", "type": "TEXT", "desc": "Treatment name"},
            {"name": "exdose", "type": "NUMERIC", "desc": "Dose amount"},
            {"name": "exdosu", "type": "TEXT", "desc": "Dose unit"},
            {"name": "exdosfrq", "type": "TEXT", "desc": "Dosing frequency"},
            {"name": "exstdtc", "type": "DATE", "desc": "Exposure start date"},
            {"name": "exendtc", "type": "DATE", "desc": "Exposure end date"},
            {"name": "visit", "type": "TEXT", "desc": "Visit name"},
            {"name": "visitnum", "type": "NUMERIC", "desc": "Visit number"},
            {"name": "arm", "type": "TEXT", "desc": "Treatment arm"},
        ]
    },
    "RPT_SV": {
        "description": "Subject visit information and schedules",
        "columns": [
            {"name": "comprehendid", "type": "TEXT", "desc": "Unique identifier"},
            {"name": "studyid", "type": "TEXT", "desc": "Study identifier"},
            {"name": "siteid", "type": "TEXT", "desc": "Site identifier"},
            {"name": "usubjid", "type": "TEXT", "desc": "Unique subject identifier"},
            {"name": "visit", "type": "TEXT", "desc": "Visit name"},
            {"name": "visitnum", "type": "NUMERIC", "desc": "Visit number"},
            {"name": "svstdtc", "type": "TIMESTAMP", "desc": "Visit start date/time"},
            {"name": "svendtc", "type": "TIMESTAMP", "desc": "Visit end date/time"},
            {"name": "visitdy", "type": "INTEGER", "desc": "Study day of visit"},
        ]
    },
    "RPT_SUBJECT_DETAIL": {
        "description": "Demographics, BMI, height, weight, status",
        "columns": [
            {"name": "comprehendid", "type": "TEXT", "desc": "Unique identifier"},
            {"name": "studyid", "type": "TEXT", "desc": "Study identifier"},
            {"name": "siteid", "type": "TEXT", "desc": "Site identifier"},
            {"name": "usubjid", "type": "TEXT", "desc": "Unique subject identifier"},
            {"name": "age", "type": "NUMERIC", "desc": "Subject age"},
            {"name": "sex", "type": "TEXT", "desc": "Subject sex (M/F)"},
            {"name": "race", "type": "TEXT", "desc": "Subject race"},
            {"name": "ethnicity", "type": "TEXT", "desc": "Subject ethnicity"},
            {"name": "bmi", "type": "NUMERIC", "desc": "Body Mass Index"},
            {"name": "height", "type": "NUMERIC", "desc": "Height"},
            {"name": "weight", "type": "NUMERIC", "desc": "Weight"},
            {"name": "arm", "type": "TEXT", "desc": "Treatment arm"},
            {"name": "sitecountry", "type": "TEXT", "desc": "Site country"},
            {"name": "siteregion", "type": "TEXT", "desc": "Site region"},
        ]
    },
    "RPT_MH": {
        "description": "Medical history and ongoing conditions",
        "columns": [
            {"name": "comprehendid", "type": "TEXT", "desc": "Unique identifier"},
            {"name": "studyid", "type": "TEXT", "desc": "Study identifier"},
            {"name": "siteid", "type": "TEXT", "desc": "Site identifier"},
            {"name": "usubjid", "type": "TEXT", "desc": "Unique subject identifier"},
            {"name": "mhterm", "type": "TEXT", "desc": "Medical history term"},
            {"name": "mhcat", "type": "TEXT", "desc": "Medical history category"},
            {"name": "mhstdtc", "type": "DATE", "desc": "Medical history start date"},
            {"name": "mhongo", "type": "TEXT", "desc": "Is condition ongoing (Yes/No)"},
        ]
    },
    "RPT_RS": {
        "description": "Response assessment and tumor measurements",
        "columns": [
            {"name": "comprehendid", "type": "TEXT", "desc": "Unique identifier"},
            {"name": "studyid", "type": "TEXT", "desc": "Study identifier"},
            {"name": "siteid", "type": "TEXT", "desc": "Site identifier"},
            {"name": "usubjid", "type": "TEXT", "desc": "Unique subject identifier"},
            {"name": "arm", "type": "TEXT", "desc": "Treatment arm"},
            {"name": "rstestcd", "type": "TEXT", "desc": "Response assessment test code"},
            {"name": "rstest", "type": "TEXT", "desc": "Response assessment test name"},
            {"name": "rscat", "type": "TEXT", "desc": "Response category"},
            {"name": "rsstresn", "type": "NUMERIC", "desc": "Standardized numeric result"},
            {"name": "rsstresu", "type": "TEXT", "desc": "Standardized unit"},
            {"name": "visit", "type": "TEXT", "desc": "Visit name"},
            {"name": "visitnum", "type": "NUMERIC", "desc": "Visit number"},
            {"name": "rsdtc", "type": "DATE", "desc": "Response assessment date"},
        ]
    },
    "RPT_GRAPHICAL_PATIENT_PROFILE": {
        "description": "Integrated patient data across domains",
        "columns": [
            {"name": "comprehendid", "type": "TEXT", "desc": "Unique identifier"},
            {"name": "studyid", "type": "TEXT", "desc": "Study identifier"},
            {"name": "studyname", "type": "TEXT", "desc": "Study name"},
            {"name": "siteid", "type": "TEXT", "desc": "Site identifier"},
            {"name": "usubjid", "type": "TEXT", "desc": "Unique subject identifier"},
            {"name": "visit", "type": "TEXT", "desc": "Visit name"},
            {"name": "domain", "type": "TEXT", "desc": "Source domain (EXPOSURE, LABS, ECG, VITAL SIGNS)"},
            {"name": "category", "type": "TEXT", "desc": "Higher-level grouping within domain"},
            {"name": "testcd", "type": "TEXT", "desc": "Standardized test code"},
            {"name": "start_date", "type": "TIMESTAMP", "desc": "Event or measurement date/time"},
        ]
    },
    "RPT_SUBJECT_DAYS": {
        "description": "Subject days on study by month",
        "columns": [
            {"name": "comprehendid", "type": "TEXT", "desc": "Unique identifier"},
            {"name": "studyid", "type": "TEXT", "desc": "Study identifier"},
            {"name": "studyname", "type": "TEXT", "desc": "Study name"},
            {"name": "siteid", "type": "TEXT", "desc": "Site identifier"},
            {"name": "sitename", "type": "TEXT", "desc": "Site name"},
            {"name": "sitecountry", "type": "TEXT", "desc": "Site country"},
            {"name": "usubjid", "type": "TEXT", "desc": "Unique subject identifier"},
            {"name": "arm", "type": "TEXT", "desc": "Treatment arm"},
            {"name": "subjectstatus", "type": "TEXT", "desc": "Current subject status"},
            {"name": "thismonth", "type": "DATE", "desc": "First day of month for calculation"},
            {"name": "thismonthsubjectdays", "type": "INTEGER", "desc": "Days on study in this month"},
            {"name": "cumulativesubjectdays", "type": "INTEGER", "desc": "Running total of subject days"},
            {"name": "totalsubjectdays", "type": "INTEGER", "desc": "Total subject days across participation"},
        ]
    },
    "RPT_AE_SEV_GRADE": {
        "description": "Adverse events with toxicity grades",
        "columns": [
            {"name": "comprehendid", "type": "TEXT", "desc": "Unique identifier"},
            {"name": "studyid", "type": "TEXT", "desc": "Study identifier"},
            {"name": "siteid", "type": "TEXT", "desc": "Site identifier"},
            {"name": "usubjid", "type": "TEXT", "desc": "Unique subject identifier"},
            {"name": "aeterm", "type": "TEXT", "desc": "Adverse event term"},
            {"name": "aeseq", "type": "INTEGER", "desc": "AE sequence number"},
            {"name": "aesev", "type": "TEXT", "desc": "AE severity"},
            {"name": "aeser", "type": "TEXT", "desc": "AE seriousness"},
            {"name": "aerelnst", "type": "TEXT", "desc": "Relationship to study intervention"},
            {"name": "aestdtc", "type": "DATE", "desc": "AE start date"},
            {"name": "aeendtc", "type": "DATE", "desc": "AE end date"},
            {"name": "faorres", "type": "TEXT", "desc": "Toxicity grade result"},
            {"name": "fatestcd", "type": "TEXT", "desc": "Toxicity test code"},
            {"name": "fatest", "type": "TEXT", "desc": "Toxicity test name"},
        ]
    },
    "RPT_STUDY_DETAILS": {
        "description": "Study metadata and CRO details",
        "columns": [
            {"name": "comprehendid", "type": "TEXT", "desc": "Unique identifier"},
            {"name": "studyid", "type": "TEXT", "desc": "Study identifier"},
            {"name": "studyname", "type": "TEXT", "desc": "Study name"},
            {"name": "studydescription", "type": "TEXT", "desc": "Study description"},
            {"name": "studystatus", "type": "TEXT", "desc": "Study status"},
            {"name": "studyphase", "type": "TEXT", "desc": "Clinical phase"},
            {"name": "studysponsor", "type": "TEXT", "desc": "Study sponsor"},
            {"name": "therapeuticarea", "type": "TEXT", "desc": "Therapeutic area"},
            {"name": "program", "type": "TEXT", "desc": "Development program"},
            {"name": "medicalindication", "type": "TEXT", "desc": "Medical indication"},
            {"name": "studystartdate", "type": "DATE", "desc": "Study start date"},
            {"name": "studycompletiondate", "type": "DATE", "desc": "Study completion date"},
            {"name": "studycro", "type": "TEXT", "desc": "CROs involved in study"},
        ]
    },
    "RPT_SUBJECT_STORY": {
        "description": "Patient journey with events timeline",
        "columns": [
            {"name": "studyid", "type": "TEXT", "desc": "Study identifier"},
            {"name": "siteid", "type": "TEXT", "desc": "Site identifier"},
            {"name": "usubjid", "type": "TEXT", "desc": "Unique subject identifier"},
            {"name": "comprehendid", "type": "TEXT", "desc": "Unique identifier"},
            {"name": "study_days", "type": "TEXT", "desc": "Study day of event"},
            {"name": "type", "type": "TEXT", "desc": "Event type (Events, Dosing, Disposition)"},
            {"name": "category", "type": "TEXT", "desc": "Event category (AE, SAE, CM, EXPOSURE)"},
            {"name": "subcategory", "type": "TEXT", "desc": "Specific event attribute name"},
            {"name": "result", "type": "TEXT", "desc": "Event attribute value"},
        ]
    },
    "RPT_TUMOR_DETAIL": {
        "description": "Tumor response assessment in oncology trials",
        "columns": [
            {"name": "comprehendid", "type": "TEXT", "desc": "Unique identifier"},
            {"name": "usubjid", "type": "TEXT", "desc": "Unique subject identifier"},
            {"name": "studyid", "type": "TEXT", "desc": "Study identifier"},
            {"name": "siteid", "type": "TEXT", "desc": "Site identifier"},
            {"name": "arm", "type": "TEXT", "desc": "Treatment arm"},
            {"name": "trlnkid", "type": "TEXT", "desc": "Lesion ID"},
            {"name": "trtest", "type": "TEXT", "desc": "Test type (LENGTH)"},
            {"name": "trorres", "type": "NUMERIC", "desc": "Measurement result for lesions"},
            {"name": "tuloc", "type": "TEXT", "desc": "Tumor location"},
            {"name": "visit", "type": "TEXT", "desc": "Visit name"},
            {"name": "visitnum", "type": "NUMERIC", "desc": "Visit number"},
            {"name": "trdtc", "type": "DATE", "desc": "Tumor measurement date"},
            {"name": "sum_of_diameters", "type": "NUMERIC", "desc": "Sum of diameters for target lesions"},
            {"name": "baseline_sod", "type": "NUMERIC", "desc": "Baseline sum of diameters"},
            {"name": "overall_response", "type": "TEXT", "desc": "Overall response (CR, PR, SD, PD, NE)"},
            {"name": "best_overall_response", "type": "TEXT", "desc": "Best overall response achieved"},
            {"name": "per_change_from_bsln_sod", "type": "NUMERIC", "desc": "Percentage change from baseline"},
        ]
    },
    "RPT_DISEASE_RESPONSE_SUMMARY": {
        "description": "Subject-level disease response flags",
        "columns": [
            {"name": "comprehendid", "type": "TEXT", "desc": "Unique identifier"},
            {"name": "studyid", "type": "TEXT", "desc": "Study identifier"},
            {"name": "siteid", "type": "TEXT", "desc": "Site identifier"},
            {"name": "usubjid", "type": "TEXT", "desc": "Unique subject identifier"},
            {"name": "arm", "type": "TEXT", "desc": "Treatment arm"},
            {"name": "subj_cr_flag", "type": "TEXT", "desc": "Complete Response flag (Yes/No)"},
            {"name": "subj_pr_flag", "type": "TEXT", "desc": "Partial Response flag (Yes/No)"},
            {"name": "subj_sd_flag", "type": "TEXT", "desc": "Stable Disease flag (Yes/No)"},
            {"name": "subj_pd_flag", "type": "TEXT", "desc": "Progressive Disease flag (Yes/No)"},
            {"name": "new_lesion_flag", "type": "TEXT", "desc": "New lesion flag (Yes/No)"},
            {"name": "treatment_status", "type": "TEXT", "desc": "Status (Death, Continue, Complete, Withdrawn)"},
        ]
    },
    "RPT_DISEASE_RESPONSE_PIVOTAL_DETAIL": {
        "description": "Tumor response with RECIST criteria",
        "columns": [
            {"name": "comprehendid", "type": "TEXT", "desc": "Unique identifier"},
            {"name": "studyid", "type": "TEXT", "desc": "Study identifier"},
            {"name": "siteid", "type": "TEXT", "desc": "Site identifier"},
            {"name": "usubjid", "type": "TEXT", "desc": "Unique subject identifier"},
            {"name": "arm", "type": "TEXT", "desc": "Treatment arm"},
            {"name": "visit", "type": "TEXT", "desc": "Visit name"},
            {"name": "visitnum", "type": "NUMERIC", "desc": "Visit number"},
            {"name": "rsdtc", "type": "DATE", "desc": "Response date"},
            {"name": "target_lesion_response", "type": "TEXT", "desc": "Target lesion response (CR, PR, SD, PD, NE)"},
            {"name": "non_target_lesion_response", "type": "TEXT", "desc": "Non-target lesion response"},
            {"name": "new_lesion", "type": "TEXT", "desc": "New lesion reported (Yes/No)"},
            {"name": "overall_response", "type": "TEXT", "desc": "Overall response from source"},
            {"name": "overall_response_derived", "type": "TEXT", "desc": "Derived overall response using RECIST"},
        ]
    },
    "RPT_MIN_GSP_DATE": {
        "description": "Min/max graphical patient profile dates",
        "columns": [
            {"name": "comprehendid", "type": "TEXT", "desc": "Unique identifier"},
            {"name": "studyid", "type": "TEXT", "desc": "Study identifier"},
            {"name": "studyname", "type": "TEXT", "desc": "Study name"},
            {"name": "siteid", "type": "TEXT", "desc": "Site identifier"},
            {"name": "usubjid", "type": "TEXT", "desc": "Unique subject identifier"},
            {"name": "date_actual", "type": "DATE", "desc": "Calculated min or max GPP date"},
            {"name": "gsp_date_type", "type": "TEXT", "desc": "Date type (min or max)"},
        ]
    },
    "RPT_CM_AE_TIMELINE": {
        "description": "Concomitant medications and AE timeline",
        "columns": [
            {"name": "comprehendid", "type": "TEXT", "desc": "Unique identifier"},
            {"name": "studyid", "type": "TEXT", "desc": "Study identifier"},
            {"name": "usubjid", "type": "TEXT", "desc": "Unique subject identifier"},
            {"name": "cmdecod", "type": "TEXT", "desc": "Decoded term (CM: or AE: prefix)"},
            {"name": "cmstdtc", "type": "DATE", "desc": "Start date (CM or AE)"},
            {"name": "cmendtc", "type": "DATE", "desc": "End date (CM or AE)"},
            {"name": "datacode", "type": "TEXT", "desc": "Domain identifier (CM or AE)"},
            {"name": "aesevcode", "type": "INTEGER", "desc": "Numeric severity code for AE (1-4)"},
            {"name": "aeser", "type": "TEXT", "desc": "AE seriousness"},
            {"name": "aerelnst", "type": "TEXT", "desc": "AE relatedness"},
            {"name": "visit", "type": "TEXT", "desc": "Visit name"},
            {"name": "visitnum", "type": "NUMERIC", "desc": "Visit number"},
            {"name": "dategsp", "type": "DATE", "desc": "Timeline date point (start or end)"},
        ]
    },
    "RPT_MH_TIMELINE": {
        "description": "Medical history timeline",
        "columns": [
            {"name": "comprehendid", "type": "TEXT", "desc": "Unique identifier"},
            {"name": "studyid", "type": "TEXT", "desc": "Study identifier"},
            {"name": "studyname", "type": "TEXT", "desc": "Study name"},
            {"name": "siteid", "type": "TEXT", "desc": "Site identifier"},
            {"name": "usubjid", "type": "TEXT", "desc": "Unique subject identifier"},
            {"name": "mhdecod", "type": "TEXT", "desc": "Decoded medical condition term"},
            {"name": "mhstdtc", "type": "DATE", "desc": "Medical condition start date"},
            {"name": "mhendtc", "type": "DATE", "desc": "Medical condition end date"},
            {"name": "mhseq", "type": "INTEGER", "desc": "Medical history sequence number"},
            {"name": "dategsp", "type": "DATE", "desc": "Timeline date point (start or end)"},
        ]
    },
}

def format_tables_for_llm() -> str:
    formatted = "Available Tables:\n"
    for i, t in enumerate(TABLES_INFO, 1):
        formatted += f"{i}. {t['table']}: {t['desc']}\n"
    return formatted


def get_table_columns(table_name: str) -> Dict:
    return TABLE_COLUMNS.get(table_name, {})

#TODO: I need to cross check this later. looks a bit unnessesary to format the table columns for llm
def format_table_columns_for_llm(table_names: List[str]) -> str:
    result = []
    for table_name in table_names:
        table_info = TABLE_COLUMNS.get(table_name)
        if table_info:
            result.append(f"Table: {table_name}")
            result.append(f"Description: {table_info['description']}")
            result.append("Columns:")
            for col in table_info['columns']:
                result.append(f"  - {col['name']} ({col['type']}): {col['desc']}")
            result.append("")
    return "\n".join(result)


PROHIBITED_KEYWORDS = [
    'insert', 'update', 'delete', 'drop', 'truncate', 'alter', 'create', 'replace',
    'information_schema', 'pg_catalog', 'pg_tables', 'pg_proc', 'pg_namespace', 'pg_class',
    'table_schema', 'table_name', 'column_name', 'column_default', 'is_nullable',
    'data_type', 'udt_name', 'character_maximum_length', 'numeric_precision',
    'numeric_scale', 'datetime_precision', 'interval_type', 'collation_name',
    'grant', 'revoke', 'rollback', 'commit', 'savepoint', 'vacuum', 'analyze'
]