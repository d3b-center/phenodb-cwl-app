import traceback
from log import print_status
from utils import VariantField, PhenoDBException

# two options for variant_object
# PARSE_FULL {CHR}:{START}-{END}{REF}>{ALT}    e.g. (1:10001-10001A>C)
# PARSE_START {CHR}:{START}                    e.g. (1:10001)
PARSE_FULL = 1
PARSE_SHORT = 2

# GENOTYPE ANNOTATION ACCORDING TO ANNOVAR
GENOTYPE_HET = 'het'
GENOTYPE_HOM = 'hom'

# variant_string: the line as read from annotation file (type: String)
# variant_object: parsed version of the line, including only some TSV fields (type: String)

class AnalysisUtils(object):
    def __init__(self, field_indices, parse_format):
        self.field_indices = field_indices
        self.parse_format = parse_format

    
    # returns a list of variant_strings, the subset of second parameter that
    #     were in ALL lists in the third parameter. Or, if third parameter
    #     empty, then returns second parameter unchanged
    # variant_strings_to_find: list of variant_strings to be looked for in all samples
    # samples_variant_strings_lists: list of lists of variant_strings that 
    #     might contain items in variant_strings_to_find. each outer list corresponds to a sample,
    #     each inner list is the list of variant_strings that person has
    def variants_in_all_lists(self, variant_strings_to_find, samples_variant_strings_lists): 
        return self.check_all_lists(variant_strings_to_find, samples_variant_strings_lists, True)


    # returns list of all variants in vars_to_find that were NOT in ANY other sample
    #     or if no samples_variants given, returns original vars_to_find
    # vars_to_find: list of variants to be looked for in all samples
    # samples_variants: list of lists of unformatted variants that might contain vars_to_find
    def variants_not_in_any_list(self, variant_strings_to_find, samples_variant_strings_lists):
        return self.check_all_lists(variant_strings_to_find, samples_variant_strings_lists, False)
        
    
    def check_all_lists(self, variant_strings_to_find, samples_variant_strings_lists, all_flag): 
        if not samples_variant_strings_lists:
            return variant_strings_to_find
        else:
            samples_variant_objects_sets = self.samples_variants_to_sets(samples_variant_strings_lists)
            variant_strings_in_samples = []
            for var_string in variant_strings_to_find:
                if all_flag and (self.var_in_all_sets(var_string, samples_variant_objects_sets)):
                    variant_strings_in_samples.append(var_string)
                if (not all_flag) and (self.var_in_no_set(var_string, samples_variant_objects_sets)):
                    variant_strings_in_samples.append(var_string)
            return variant_strings_in_samples
        
    
    # returns True if the variant is in ALL of the sets
    # variant_string: variant_string to look for in the sets
    # samples_variant_objects_sets: list of variant_objects sets to be searched
    def var_in_all_sets(self, variant_string, samples_variant_objects_sets):
        return self.check_sets(variant_string, samples_variant_objects_sets, True)
    

    # returns True if the variant is in ANY of the sets
    # variant_string: variant_string to look for in the sets
    # samples_variant_objects_sets: list of variant_objects sets to be searched
    def var_in_no_set(self, variant_string, samples_variant_objects_sets):
        return self.check_sets(variant_string, samples_variant_objects_sets, False)
    
    
    def check_sets(self, variant_string, samples_variant_objects_sets, all_flag):
         variant_object = self.parse_variant(variant_string)
         for variant_objects_set in samples_variant_objects_sets:
             if all_flag and (variant_object not in variant_objects_set):
                 return False
             if (not all_flag) and (variant_object in variant_objects_set):
                 return False
         return True
    

    # returns: list of sets of variant_objects
    # samples_variant_strings_lists: list of lists of variant_strings
    def samples_variants_to_sets(self, samples_variant_strings_lists):
        samples_variant_objects_sets = []
        for variant_strings_list in samples_variant_strings_lists:
            variant_objects_set = set()
            for var in variant_strings_list:
                variant_objects_set.add(self.parse_variant(var))
            samples_variant_objects_sets.append(variant_objects_set)
        return samples_variant_objects_sets


    # returns: variant_object, with only the fields to use in comparison
    # gets only select fields from the tab-separated variant string
    # in order to build comparable strings, since some variants might have additional fields
    # that should not be used for the comparison
    # format to use is set in the Analyzer's constructor
    def parse_variant(self, var_string):
        try:
            chromosome = var_string.split("\t")[self.field_indices[VariantField.CHR]]
            start = var_string.split("\t")[self.field_indices[VariantField.START]]
            chr_num = chromosome

            if chromosome.capitalize().startswith("CHR"):
                chr_num = chromosome.capitalize().replace("CHR", "")

            parsed_variant = chr_num + ":" + start

            if self.parse_format == PARSE_FULL:
                end = var_string.split("\t")[self.field_indices[VariantField.END]]
                ref = var_string.split("\t")[self.field_indices[VariantField.REF]]
                alt = var_string.split("\t")[self.field_indices[VariantField.ALT]]
                parsed_variant += "-" + end + ref + ">" + alt

            return parsed_variant
        except:
            traceback.print_stack()
            raise PhenoDBException('Unable to parse variant:', var_string)
    

    def get_genotype(self, var):
        try:
            return var.split("\t")[self.field_indices[VariantField.GT]]
        except:
            raise PhenoDBException('Unable to parse genotype from variant:', var)
        

    def get_zygosity_matches(self, variant_strings, zygosity, append_log, log_text):
        zygosity_matches = []
        i = 0
        for var in variant_strings:
            i += 1
            if self.get_genotype(var) == zygosity:
                zygosity_matches.append(var)
        print_status('analyzer.get_heterozygous_vars()', i, '')
        if append_log:
            log_text.append_text(
                'Including {0} in Genotype {1} variants -> {2} variants'.format(
                    zygosity, str(len(variant_strings)), str(len(zygosity_matches))))
        return zygosity_matches