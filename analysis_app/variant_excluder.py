from utils import VariantField

# exclude variants based on user selected criteria
class VariantExcluder(object):
    def __init__(self, field_indices, maf_cutoff, refgene_gene_locations):
        self.field_indices = field_indices  # dictionary with indices with fields of interest
        self.maf_cutoff = maf_cutoff
        self.refgene_gene_locations = refgene_gene_locations
        self.treat_as_zero = set([".", "\t", "\n", ".\n"])  # MAF values to parse into 0.0


    # TODO make this clearer to read
    def filter(self, variants, log):
        filtered_gene_location = self.filter_refgene_gene_location(variants, log)
        filtered_exon_function = self.filter_refgene_exon_function(filtered_gene_location, log)
        filtered_maf_cutoff = self.filter_maf(filtered_exon_function, log)
        return filtered_maf_cutoff


    # return all variants whose refgene_gene_location is one of the selected options
    def filter_refgene_gene_location(self, variants, log):
        gene_location_filtered = []

        for var in variants:
            var_refgene_gene_location = var.split("\t")[self.field_indices[VariantField.REF_GENE_LOC]]
            if var_refgene_gene_location in self.refgene_gene_locations:
                gene_location_filtered.append(var)

        log.append_text(
            'Including {0} in RefGeneLocation, {1} variants -> {2} variants'.format(self.refgene_gene_locations,
                                                                                    str(len(variants)),
                                                                                    str(len(gene_location_filtered))))

        return gene_location_filtered


    # synonymous variants can be relevant in the case of 'exonic;splicing'
    # because they might change how splicing occurs
    def filter_refgene_exon_function(self, variants, log):
        exon_function_removed = []

        for var in variants:
            if self.check_refgene_exon_function(var):
                exon_function_removed.append(var)

        log.append_text(
            'Excluding synonymous SNV in RefGeneExonFunction, except for exonic:splicing variants {0} variants -> {1} variants'.format(
                str(len(variants)), str(len(exon_function_removed))))

        return exon_function_removed


    def check_refgene_exon_function(self, line):
        refgene_gene_location = line.split("\t")[self.field_indices[VariantField.REF_GENE_LOC]]
        refgene_exon_function = line.split("\t")[self.field_indices[VariantField.REF_GENE_EXON_FUNC]]

        if refgene_exon_function == "synonymous SNV":
            if refgene_gene_location == "exonic;splicing":
                return True
            else:
                return False
        else:
            return True

    
    # exclude variants whose MAF is above cutoff set by user
    def filter_maf(self, variants, log):
        maf_cutoff_removed = []

        for var in variants:
            keep_variant = True
            for maf_index in self.field_indices[VariantField.MAF]:  # multiple indices can contain MAF, any of them can exclude the variant
                if self.maf_format(var.split("\t")[maf_index]) > self.maf_cutoff:
                    keep_variant = False
                    break
            if keep_variant:
                maf_cutoff_removed.append(var)

        log.append_text(
            'Excluding if value is greater than, {0} in selected MAF projects, {1} variants -> {2} variants'.format(
                self.maf_cutoff, str(len(variants)), str(len(maf_cutoff_removed))))

        return maf_cutoff_removed


    # parse string with variant's MAF into a float
    def maf_format(self, maf_string):
        if (maf_string in self.treat_as_zero) or (not maf_string):
            return 0.0
        else:
            return float(maf_string)
