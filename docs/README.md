# WXO Healthcare MCP Hackathon

You have **20–30 minutes**. The goal is to build something useful in watsonx Orchestrate using a live MCP server backed by a fictional hospital database.

---

## Step 1 — Connect the MCP Server

1. Open your watsonx Orchestrate instance in a browser.
2. Click **☰ menu → Build → All tools → Create Tool + → MCP Server → Add MCP Server + → Local MCP Server → Next**.
3. Fill in the form:

   | Field | Value |
   |---|---|
   | **Server name** | `healthcare-mcp` |
   | **Description** | `Hospital data MCP server` |
   | **Install Command** | `uvx --from wxo-bootcamp-mcp-server wxo-bootcamp-data-server-stdio` |
   | **Select Connection (optional)** | Leave blank |

4. Click **Add** and wait for the tools to import.

---

## Step 2 — Understand the Tools

Open the **[Tool Reference](https://htmlpreview.github.io/?https://github.com/Nniol/wxo-bootcamp-mcp-server/blob/main/docs/healthcare_mcp_tools.html)** for the full interactive tool reference.

There are **8 tools** available:

| Tool | What it does |
|------|-------------|
| `wxoGetPatientInformation` | Demographics, contact, insurance for a patient |
| `wxoGetMedicalInformation` | Diagnoses, prescriptions, allergies, medical history |
| `wxoGetVitalSignsInformation` | Latest recorded vitals |
| `wxoGetDrugInformation` | Drug details — dosage, side effects, class |
| `wxoGetDrugInteractions` | Interaction check between two drugs |
| `wxoGetDrugContraindications` | Contraindications for a drug given a condition |
| `wxoGetDrugAlternativeTreatments` | Alternative drugs for a condition |
| `wxoGetPatient360` | Full patient snapshot in one call |

Patient IDs follow the format **PAT + 3 digits** for 7 patients (e.g. `PAT001`, `PAT002`, ... , `PAT007`).

---

## Step 3 — Build

Design and wire up agents in WXO that use these tools. What you build is up to you — the tool reference has suggested workflows if you want a starting point.

Some directions to consider:
- A clinical triage agent that summarises a patient's situation
- A drug safety checker that flags interactions and suggests alternatives
- A handoff flow that routes a patient summary to the right specialist

---

## Notes

- All patient data is entirely fictional — no relation to any real person
- The server runs stateless STDIO — each call is independent
- If a patient ID doesn't exist the tools return `None`
