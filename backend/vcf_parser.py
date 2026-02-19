def parse_vcf(file_content):
    variants = []

    for line in file_content.splitlines():

        if not line.strip():
            continue

        if line.startswith("#"):
            continue

        parts = line.split("\t")

        # Ensure minimum VCF columns exist
        if len(parts) < 8:
            continue

        info_field = parts[7]

        info_dict = {}

        for item in info_field.split(";"):
            if "=" in item:
                key, value = item.split("=", 1)
                info_dict[key] = value

        if "GENE" in info_dict:
            variants.append({
                "gene": info_dict.get("GENE"),
                "rsid": info_dict.get("RS"),
                "star": info_dict.get("STAR")
            })

    return variants
