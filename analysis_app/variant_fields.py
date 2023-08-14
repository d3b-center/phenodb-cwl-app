from utils import PhenoDBException, VariantField

# parse the TSV header of an ANNOVAR file to to get the indices of these target fields
# stores the indices of TSV fields in ANNOVAR variant strings to be used in analysis
# variants are used throughout the application as only tab-separated strings
# values of interest in the variants are obtained using the item's string-TSV-index from this class


# key is a VariantFields enum
# value is an int index for all, except MAF which is a set of int indices
field_indices = {
    VariantField.CHR: None,
    VariantField.START: None,
    VariantField.END: None,
    VariantField.REF: None,
    VariantField.ALT: None,
    VariantField.GT: None,
    VariantField.REF_GENE_LOC: None,
    VariantField.REF_GENE_NAME: None,
    VariantField.REF_GENE_EXON_FUNC: None,
    VariantField.MAF: set()  # set of ints
}

def check_missing_fields(fields_indices):
    none_fields = []
    for key, value in fields_indices.items():
        if value is None:
            none_fields.append(key)
    return none_fields


def get_variants_fields(vcf_file):
    header_string = get_header_string(vcf_file)
    header_fields = header_string.split('\t')
    n = 0
    for field in header_fields:
        vf = VariantField.from_string(field)
        if vf == VariantField.MAF:
            field_indices[VariantField.MAF].add(n)
        elif vf is not None:
            field_indices[vf] = n
        n += 1
    missing_fields = check_missing_fields(field_indices)
    if missing_fields:
        raise PhenoDBException('Required variant field(s) missing from VCF:', str(missing_fields))
    else:
        return field_indices


def get_header_string(vcf_file_path):
    header_string = ''
    try:
        with open(vcf_file_path, 'r') as f:
            for line in f.readlines():
                if line.startswith('Chromosome') or line.startswith('Chr'):
                    header_string = line
                    break
        if header_string == '':
            raise PhenoDBException('Header not found in file:', vcf_file_path)
        return header_string
    except:
        raise PhenoDBException('File not found:', vcf_file_path)
