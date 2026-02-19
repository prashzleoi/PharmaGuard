import os
from groq import Groq

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY not found in environment variables")

client = Groq(api_key=api_key)




def generate_explanation(drug, risk, variants=None):

    gene = risk.get("primary_gene", "Unknown")
    phenotype = risk.get("phenotype", "Unknown")
    risk_label = risk.get("risk_label", "Unknown")

    # Extract RSIDs for variant-level explanation
    variant_ids = []
    if variants:
        variant_ids = [
            v.get("rsid") for v in variants if v.get("rsid")
        ]

    variant_section = ""
    if variant_ids:
        variant_section = (
            f"The following pharmacogenomic variants were detected: "
            f"{', '.join(variant_ids)}. "
            f"These variants may alter {gene} enzyme activity."
        )
    else:
        variant_section = (
            "No high-impact pharmacogenomic variants were detected in the target gene."
        )

    prompt = f"""
You are a clinical pharmacogenomics expert.

Drug: {drug}
Primary Gene: {gene}
Phenotype: {phenotype}
Risk classification: {risk_label}

Variant Information:
{variant_section}

Provide a structured clinical explanation including:

1. Drug mechanism of action
2. Role of {gene} in metabolism
3. Impact of detected variants (if any)
4. Why the phenotype leads to this risk classification
5. A CPIC-aligned clinical recommendation

Be medically accurate, precise, and concise.
"""

    chat = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    return {
        "summary": chat.choices[0].message.content
    }
