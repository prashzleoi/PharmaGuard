GENE_DRUG_MAP = {
    "CODEINE": "CYP2D6",
    "WARFARIN": "CYP2C9",
    "CLOPIDOGREL": "CYP2C19",
    "SIMVASTATIN": "SLCO1B1",
    "AZATHIOPRINE": "TPMT",
    "FLUOROURACIL": "DPYD"
}


# ==============================
# Variant → Phenotype Mapping
# ==============================

LOSS_OF_FUNCTION_VARIANTS = {
    "CYP2C19": ["rs4244285"],
    "CYP2C9": ["rs1799853"],
    "CYP2D6": ["rs3892097"],
    "SLCO1B1": ["rs4149056"],
    "TPMT": ["rs1142345"],
    "DPYD": ["rs3918290"]
}

VKORC1_SENSITIVITY_VARIANT = "rs9923231"


def assess_risk(drug, variants):

    drug = drug.upper()

    if drug not in GENE_DRUG_MAP:
        return {
            "risk_label": "Unknown",
            "confidence_score": 0.0,
            "severity": "none",
            "primary_gene": None,
            "diplotype": "Unknown",
            "phenotype": "Unknown",
            "detected_variants": []
        }

    target_gene = GENE_DRUG_MAP[drug]

    # Collect gene-specific variants
    matching_variants = [
        v for v in variants if v["gene"] == target_gene
    ]

    # ==============================
    # WARFARIN SPECIAL CASE (CYP2C9 + VKORC1)
    # ==============================
    if drug == "WARFARIN":

        cyp2c9_variants = [
            v for v in variants if v["gene"] == "CYP2C9"
        ]

        vkorc1_variants = [
            v for v in variants if v.get("rsid") == VKORC1_SENSITIVITY_VARIANT
        ]

        phenotype = "NM"
        risk_label = "Safe"
        severity = "low"
        detected = cyp2c9_variants + vkorc1_variants

        # CYP2C9 loss of function
        if any(v["rsid"] in LOSS_OF_FUNCTION_VARIANTS["CYP2C9"]
               for v in cyp2c9_variants):
            phenotype = "IM"
            risk_label = "Adjust Dosage"
            severity = "moderate"

        # VKORC1 sensitivity
        if vkorc1_variants:
            risk_label = "Adjust Dosage"
            severity = "moderate"

        return {
            "risk_label": risk_label,
            "confidence_score": 0.9,
            "severity": severity,
            "primary_gene": "CYP2C9 & VKORC1",
            "diplotype": "*1/*2" if phenotype != "NM" else "*1/*1",
            "phenotype": phenotype,
            "detected_variants": detected
        }

    # ==============================
    # NO VARIANTS FOUND
    # ==============================
    if not matching_variants:
        return {
            "risk_label": "Safe",
            "confidence_score": 0.7,
            "severity": "low",
            "primary_gene": target_gene,
            "diplotype": "*1/*1",
            "phenotype": "NM",
            "detected_variants": []
        }

    # ==============================
    # Variant-Based Classification
    # ==============================

    has_lof = any(
        v["rsid"] in LOSS_OF_FUNCTION_VARIANTS.get(target_gene, [])
        for v in matching_variants
    )

    # FLUOROURACIL (DPYD) – Toxic if LOF
    if drug == "FLUOROURACIL" and has_lof:
        return {
            "risk_label": "Toxic",
            "confidence_score": 0.95,
            "severity": "critical",
            "primary_gene": target_gene,
            "diplotype": "*1/*2A",
            "phenotype": "PM",
            "detected_variants": matching_variants
        }

    # CLOPIDOGREL – Ineffective if LOF
    if drug == "CLOPIDOGREL" and has_lof:
        return {
            "risk_label": "Ineffective",
            "confidence_score": 0.9,
            "severity": "moderate",
            "primary_gene": target_gene,
            "diplotype": "*1/*2",
            "phenotype": "IM",
            "detected_variants": matching_variants
        }

    # CODEINE – Adjust if LOF
    if drug == "CODEINE" and has_lof:
        return {
            "risk_label": "Adjust Dosage",
            "confidence_score": 0.9,
            "severity": "moderate",
            "primary_gene": target_gene,
            "diplotype": "*1/*4",
            "phenotype": "IM",
            "detected_variants": matching_variants
        }

    # SIMVASTATIN – Myopathy risk
    if drug == "SIMVASTATIN" and has_lof:
        return {
            "risk_label": "Adjust Dosage",
            "confidence_score": 0.85,
            "severity": "moderate",
            "primary_gene": target_gene,
            "diplotype": "*1/*5",
            "phenotype": "IM",
            "detected_variants": matching_variants
        }

    # AZATHIOPRINE – TPMT risk
    if drug == "AZATHIOPRINE" and has_lof:
        return {
            "risk_label": "Adjust Dosage",
            "confidence_score": 0.9,
            "severity": "moderate",
            "primary_gene": target_gene,
            "diplotype": "*1/*3A",
            "phenotype": "IM",
            "detected_variants": matching_variants
        }

    # Default fallback
    return {
        "risk_label": "Adjust Dosage",
        "confidence_score": 0.85,
        "severity": "moderate",
        "primary_gene": target_gene,
        "diplotype": "*1/*2",
        "phenotype": "IM",
        "detected_variants": matching_variants
    }