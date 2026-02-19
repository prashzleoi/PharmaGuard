from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware
import uuid

from vcf_parser import parse_vcf
from risk_engine import assess_risk
from llm_explainer import generate_explanation

app = FastAPI()
templates = Jinja2Templates(directory="../frontend/templates")

MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For hackathon demo
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# =========================================
# Enhanced CPIC Clinical Recommendation Engine
# =========================================
def get_clinical_recommendation(drug, phenotype):
    drug = drug.upper()

    # CYP2C19 – CLOPIDOGREL
    if drug == "CLOPIDOGREL":
        if phenotype in ["IM", "PM"]:
            return {
                "action": "Use alternative antiplatelet therapy (prasugrel or ticagrelor)",
                "guideline_source": "CPIC Level A – CYP2C19 & Clopidogrel"
            }
        return {
            "action": "Standard dosing recommended",
            "guideline_source": "CPIC Level A – CYP2C19 & Clopidogrel"
        }

    # CYP2C9 – WARFARIN
    if drug == "WARFARIN":
        if phenotype in ["IM", "PM"]:
            return {
                "action": "Reduce initial dose and monitor INR closely",
                "guideline_source": "CPIC Level A – CYP2C9 & Warfarin"
            }
        return {
            "action": "Standard dosing recommended",
            "guideline_source": "CPIC Level A – CYP2C9 & Warfarin"
        }

    # CYP2D6 – CODEINE
    if drug == "CODEINE":

        if phenotype == "PM":
            return {
                "action": "Avoid codeine due to lack of efficacy",
                "guideline_source": "CPIC Level A – CYP2D6 & Codeine"
            }

        if phenotype == "URM":
            return {
                "action": "Avoid codeine due to toxicity risk",
                "guideline_source": "CPIC Level A – CYP2D6 & Codeine"
            }

        if phenotype == "IM":
            return {
                "action": "Consider reduced dose or alternative opioid",
                "guideline_source": "CPIC Level A – CYP2D6 & Codeine"
            }

        return {
            "action": "Standard dosing recommended",
            "guideline_source": "CPIC Level A – CYP2D6 & Codeine"
        }

    # SLCO1B1 – SIMVASTATIN
    if drug == "SIMVASTATIN":
        if phenotype in ["IM", "PM"]:
            return {
                "action": "Consider lower dose or alternative statin due to myopathy risk",
                "guideline_source": "CPIC Level A – SLCO1B1 & Simvastatin"
            }
        return {
            "action": "Standard dosing recommended",
            "guideline_source": "CPIC Level A – SLCO1B1 & Simvastatin"
        }

    # TPMT – AZATHIOPRINE
    if drug == "AZATHIOPRINE":
        if phenotype == "PM":
            return {
                "action": "Substantially reduce dose or consider alternative therapy",
                "guideline_source": "CPIC Level A – TPMT & Azathioprine"
            }
        if phenotype == "IM":
            return {
                "action": "Reduce starting dose and monitor closely",
                "guideline_source": "CPIC Level A – TPMT & Azathioprine"
            }
        return {
            "action": "Standard dosing recommended",
            "guideline_source": "CPIC Level A – TPMT & Azathioprine"
        }

    # DPYD – FLUOROURACIL
    if drug == "FLUOROURACIL":
        if phenotype in ["IM", "PM"]:
            return {
                "action": "Reduce starting dose due to toxicity risk",
                "guideline_source": "CPIC Level A – DPYD & Fluorouracil"
            }
        return {
            "action": "Standard dosing recommended",
            "guideline_source": "CPIC Level A – DPYD & Fluorouracil"
        }

    return {
        "action": "Adjust therapy based on clinical judgment",
        "guideline_source": "CPIC"
    }




@app.post("/analyze")
async def analyze(file: UploadFile = File(...), drug: str = Form(...)):

    # 1️⃣ Validate extension
    if not file.filename.endswith(".vcf"):
        return JSONResponse(
            {"error": "Invalid file format. Please upload a .vcf file."},
            status_code=400
        )

    content = await file.read()

    # 2️⃣ Validate size
    if len(content) > MAX_FILE_SIZE:
        return JSONResponse(
            {"error": "File exceeds 5MB size limit."},
            status_code=400
        )

    decoded_content = content.decode(errors="ignore")

    # 3️⃣ Validate VCF header
    if not decoded_content.startswith("##fileformat=VCFv4.2"):
        return JSONResponse(
            {"error": "Invalid VCF file structure. Must be VCF v4.2."},
            status_code=400
        )

    # 4️⃣ Parse VCF
    try:
        variants = parse_vcf(decoded_content)
    except Exception:
        return JSONResponse(
            {"error": "Error parsing VCF file."},
            status_code=400
        )

    if variants is None:
        variants = []

    drugs = [d.strip() for d in drug.split(",") if d.strip()]
    results = []

    for d in drugs:
        risk = assess_risk(d, variants)

        detected_variants = risk.get("detected_variants", [])

        explanation_text = generate_explanation(
            drug=d,
            risk=risk,
            variants=detected_variants
        )

        recommendation = get_clinical_recommendation(
            d,
            risk.get("phenotype", "Unknown")
        )

        result = {
            "patient_id": str(uuid.uuid4()),
            "drug": d,
            "timestamp": datetime.utcnow().isoformat(),
            "risk_assessment": {
                "risk_label": risk.get("risk_label", "Unknown"),
                "confidence_score": risk.get("confidence_score", 0.0),
                "severity": risk.get("severity", "none")
            },
            "pharmacogenomic_profile": {
                "primary_gene": risk.get("primary_gene"),
                "diplotype": risk.get("diplotype", "Unknown"),
                "phenotype": risk.get("phenotype", "Unknown"),
                "detected_variants": detected_variants
            },
            "clinical_recommendation": recommendation,
            "llm_generated_explanation": {
                "summary": explanation_text.get("summary", ""),
                "variant_references": [
                    v.get("rsid") for v in detected_variants if v.get("rsid")
                ]
            },
            "quality_metrics": {
                "vcf_parsing_success": True,
                "variant_count": len(variants),
                "gene_variants_detected": len(detected_variants),
                "drug_processed": True,
                "multiple_drugs_supported": len(drugs) > 1
            }
        }

        results.append(result)

    return JSONResponse(results)