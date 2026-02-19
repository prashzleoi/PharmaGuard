🧬 PharmaGuard
Precision Medicine Powered by Hybrid AI

Transforming genomic data into actionable, explainable clinical decisions.

🌐 Live Demo (Backend API):
https://pharmaguard-urhd.onrender.com

📦 GitHub Repository:
https://github.com/prashzleoi/PharmaGuard

Live-link : 
pharmaguardz.netlify.app

🚀 Overview

PharmaGuard is an AI-driven pharmacogenomics decision support system that analyzes patient VCF files and generates CPIC-aligned therapeutic recommendations with explainable AI insights.

Unlike generic AI tools, PharmaGuard uses a hybrid architecture:

✅ Deterministic CPIC-based rule engine for clinical safety

✅ Variant-aware phenotype classification

✅ LLM-powered explainable medical reasoning (Groq)

✅ Real-time risk stratification

This ensures medical reliability while maintaining interpretability.

🧠 Problem

Adverse Drug Reactions (ADRs) account for:

~5–10% of hospital admissions globally

Billions in healthcare costs

Preventable toxicity due to genetic variability

Most prescribing is still trial-and-error.

Genomic data exists — but it's not clinically translated in real time.

💡 Solution

PharmaGuard converts raw genomic VCF data into:

Drug-specific metabolic phenotype

Risk classification (Safe / Adjust Dosage / Ineffective / Toxic)

CPIC-aligned dosing guidance

Structured JSON for integration

Explainable AI summary for clinicians

🧬 Supported CPIC Level A Gene–Drug Pairs
Drug	Gene	Clinical Risk
CODEINE	CYP2D6	Toxicity / Ineffective
WARFARIN	CYP2C9 (+ VKORC1 ready)	Bleeding Risk
CLOPIDOGREL	CYP2C19	Reduced Efficacy
SIMVASTATIN	SLCO1B1	Myopathy
AZATHIOPRINE	TPMT	Myelosuppression
FLUOROURACIL	DPYD	Severe Toxicity
🏗 Architecture

Frontend (Netlify-ready UI)
⬇
FastAPI Backend (Render deployment)
⬇
VCF Parser
⬇
Rule-Based CPIC Risk Engine
⬇
LLM Explanation Layer (Groq API)

Hybrid Design Principle

Clinical decisions are rule-based and deterministic.
The LLM only generates structured explanation — never dosing decisions.

This eliminates AI hallucination risk in therapeutic classification.

📊 Example Output
{
  "drug": "FLUOROURACIL",
  "risk_label": "Toxic",
  "phenotype": "PM",
  "gene": "DPYD",
  "recommendation": "Reduce starting dose due to toxicity risk"
}
🔬 How It Works

Upload VCF v4.2 file

Validate format and size (≤5MB)

Parse actionable pharmacogenomic variants

Map gene → phenotype → risk classification

Apply CPIC guideline logic

Generate structured clinical recommendation

Generate variant-aware explanation via Groq LLM

⚙ Tech Stack

Backend:

FastAPI

Uvicorn

Python 3

Groq API (LLaMA 3.1 8B Instant)

CPIC-based rule engine

Frontend:

TailwindCSS

Glassmorphism UI

Dynamic JSON export

Drag & drop VCF upload

Deployment:

Render (Backend)

Netlify (Frontend-ready)

GitHub version control

🔐 Security Considerations

API keys stored via environment variables

No patient data persisted

VCF processed in-memory only

CORS enabled for demo mode

🧪 Demo Scenarios

✅ Normal Metabolizer (NM) → Standard dosing
⚠ Intermediate Metabolizer (IM) → Adjust dosage
🚨 Poor Metabolizer (PM) → Avoid / Reduce dose

🏆 Hackathon Highlights

Fully functional pharmacogenomic engine

Hybrid deterministic + AI architecture

Clinically aligned with CPIC Level A guidelines

Scalable API design

Multi-drug support

JSON export for EHR integration

📈 Future Improvements

VKORC1 integration for Warfarin

CPIC live guideline sync

EHR integration (FHIR compatible)

Clinical validation dataset

Regulatory pathway modeling

Multi-patient batch processing

🧠 Why This Is Different

This is NOT:

A ChatGPT wrapper

A text-based AI explanation tool

A static drug database

This IS:

A structured pharmacogenomics decision support system with explainable AI.

⚠ Disclaimer

PharmaGuard is a prototype clinical decision-support tool built for research and educational purposes.
It is not approved for real-world medical use.

👨‍💻 Author

Built by Prasanth Kumar
AI + Precision Medicine Enthusiast
