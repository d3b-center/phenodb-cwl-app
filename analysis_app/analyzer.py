from compound_analysis_utils import *
from analysis_utils import AnalysisUtils, PARSE_SHORT, GENOTYPE_HOM, GENOTYPE_HET
from log import print_status
from utils import AffectedStatus, AnalysisType, FamilyMember, PhenoDBException, VariantField, debug_log


PARENTS = [FamilyMember.Mother, FamilyMember.Father]


# AR_CH: all variants appearing at least twice in a gene in the same pattern
#     in all affected samples, and not found in that pattern in any unaffected sample
# AR_H: all variants found on all affected individuals as homozygous and not found on unaffected
#     individuals as homozygous
# AD_NM: all variants found on proband not present on parents (only applied for trio analysis)
# AD_IM: all variants found on affected samples and not found on unaffected samples (applied for
#     multiples affected individuals in the family)
# AD_V: all heterozygous variants present on proband


class Analyzer(object):
    def __init__(self, all_samples, field_indices):
        self.variant_format = PARSE_SHORT
        self.field_indices = field_indices
        self.analyzer = AnalysisUtils(field_indices, self.variant_format)
        self.all_samples = all_samples
        # groups of samples often used together
        self.affected = []    # affected samples, excluding proband
        self.unaffected = []  # unaffected samples
        self.non_proband = []  # all samples other than proband
        self.proband = None
        self.assign_samples()  # populate affected, unaffected, proband, non_proband
        self.proband_vars = self.proband.variants

    def analyze_variants(self, analysis_type, log):
        if analysis_type is AnalysisType.AD_V:
            return self.run_AD_V(log)
        elif analysis_type == AnalysisType.AD_IM:
            return self.run_AD_IM(log)
        elif analysis_type == AnalysisType.AD_NM:
            return self.run_AD_NM(log)
        elif analysis_type == AnalysisType.AR_H:
            return self.run_AR_H(log)
        elif analysis_type == AnalysisType.AR_CH:
            return self.run_AR_CH(log)
        else:
            raise PhenoDBException('Invalid analysis type:', analysis_type)

    #
    # ---------------- 1. AD_V ----------------
    # only uses proband
    # returns all proband's heterozygous variants
    def run_AD_V(self, log):
        proband_het_vars = self.analyzer.get_zygosity_matches(self.proband_vars, GENOTYPE_HET, True, log)
        return proband_het_vars


    #
    # ---------------- 2. AD_IM ----------------
    # requires proband and at least one relative, who can be either affected or not
    # returns variants shared by only affected people, not unaffected
    def run_AD_IM(self, log):
        # -------- 2.a. get proband's heterozygous variants --------
        proband_het_vars = self.analyzer.get_zygosity_matches(self.proband_vars, GENOTYPE_HET, True, log)

        # -------- 2.b. exclude variants NOT in ALL other affected samples --------
        affected_samples_variants = []
        for sample_affected in self.affected:
            affected_samples_variants.append(sample_affected.variants)
        
        vars_all_affected = self.analyzer.variants_in_all_lists(proband_het_vars, affected_samples_variants)

        log.append_text(
            'Including if start position is in all affected members with het Genotype {0} variants -> {1} variants'.format(
                str(len(proband_het_vars)), str(len(vars_all_affected))))

        # -------- 2.c. exclude variants in ANY unaffected sample --------
        unaffect_samples_variants = []
        for sample_unaffect in self.unaffected:
            unaffect_samples_variants.append(sample_unaffect.variants)

        AD_IM_result_vars = self.analyzer.variants_not_in_any_list(vars_all_affected, unaffect_samples_variants)

        log.append_text('Excluding if start position is in any unaffected members with hom Genotype, {0} variants -> {1} variants'.format(
            str(len(vars_all_affected)), str(len(AD_IM_result_vars))))
        
        print_status('analysisDriver.run_AD_IM()', None, '')
        return AD_IM_result_vars


    #
    # ---------------- 3. AD_NM ----------------
    # only parent samples are analyzed, and both are required
    # returns variants (het and hom) that only the proband has
    def run_AD_NM(self, log):
        proband_het_hom = []

        # -------- 3.a. get proband's heterozygous and homozygous variants --------
        i_3_a = 0
        for var in self.proband_vars:
            i_3_a += 1
            genotype = var.split("\t")[self.field_indices[VariantField.GT]]
            if genotype == GENOTYPE_HET or genotype == GENOTYPE_HOM:  # TODO replace with list check
                proband_het_hom.append(var)

        log.append_text('Including {0}, {1} in Genotype, {2} variants -> {3} variants'.format(
            GENOTYPE_HET, GENOTYPE_HOM, str(len(self.proband_vars)), str(len(proband_het_hom))))
        print_status('analysisDriver.run_AD_NM() 3_a', i_3_a, '')

        # -------- 3.b. exclude variants in any parent sample --------
        # pass samples one at a time to get printout with relationship to proband
        # skip any sample that is not a parent
        result_vars = proband_het_hom
        for sample in self.non_proband:
            if sample.family_member_id not in PARENTS:
                continue  # skip non-parents
            result_vars = self.vars_not_in_one_sample_logged(result_vars, sample, log)
        return result_vars
    

    # AD_NM helper method
    def vars_not_in_one_sample_logged(self, start_vars, sample, log):
        parent = FamilyMember(sample.family_member_id).name
        
        sample_variants = sample.variants
        vars_not_in_sample = self.analyzer.variants_not_in_any_list(start_vars, [sample_variants])
        
        log.append_text(
            'Excluding inherited from {0} {1} variants -> {2} variants'.format(
                parent, str(len(start_vars)), str(len(vars_not_in_sample))))
        print_status('analysisDriver.run_AD_NM() remove_vars_print_status', None, "")

        return vars_not_in_sample
    

    #
    # ---------------- 4. AR_H ----------------
    # requires proband only
    # returns variants for which only proband and affected non-parents are homozygous
    # affected parent samples were removed by Preprocessor
    # this checks for recessive disease (aka homozygous) 
    def run_AR_H(self, log):

        # -------- 4.a. get proband's homozygous variants --------
        proband_hom_vars = self.analyzer.get_zygosity_matches(self.proband_vars, GENOTYPE_HOM, True, log)

        # -------- 4.b. exclude variants NOT HOMOZYGOUS in ALL other affected samples --------
        affected_hom_variants_lists = []
        for sample_affected in self.affected:
            sample_all_vars = sample_affected.variants
            affected_hom_variants_lists.append(self.analyzer.get_zygosity_matches(sample_all_vars, GENOTYPE_HOM, False, log))
        
        vars_hom_all_affected = self.analyzer.variants_in_all_lists(proband_hom_vars, affected_hom_variants_lists)
        
        log.append_text(
            'Including if start position is in all affected members with hom Genotype, {0} variants -> {1} variants'.format(
                str(len(proband_hom_vars)), str(len(vars_hom_all_affected))))
        print_status('analysisDriver.run_AR_H() 4_b', None, "")

        # -------- 4.c. exclude variants HOMOZYGOUS in ANY unaffected sample --------
        unaffected_hom_variants_lists = []
        for sample_unaffect in self.unaffected:
            sample_all_vars = sample_unaffect.variants
            unaffected_hom_variants_lists.append(self.analyzer.get_zygosity_matches(sample_all_vars, GENOTYPE_HOM, False, log))
        
        result_variants = self.analyzer.variants_not_in_any_list(vars_hom_all_affected, unaffected_hom_variants_lists)

        log.append_text(
            'Excluding if start position is in any unaffected members with hom Genotype, '
            '{0} variants -> {1} variants'.format(
                str(len(vars_hom_all_affected)), str(len(result_variants))))
        print_status('analysisDriver.run_AR_H() 4_c', None, "")

        return result_variants

    #
    # ---------------- 5. AR_CH ----------------
    # Requires proband only
    # Returns combination of >= 2 variants for a gene which only affected individuals have
    def run_AR_CH(self, log):

        # -------- 5.a. get variants that meet the AD_IM pattern --------
        # proband_im = self.analyze_variants(AnalysisType.AD_IM, log_text, affected)
        proband_ad_im_vars = self.run_AD_IM(log)
        log.append_text(
            '# Note: analysis above obtained variants with AD_IM inheritance, and analysis on them for AR_CH inheritance continues below')
        print_status('analysisDriver.run_AR_CH() 5_a run_AD_IM', None, "")

        # -------- 5.b. get proband's genes that have multiple variants --------
        compound_utils = CompoundAnalyzerUtils(self.analyzer)
        
        proband_all_genes_dict = compound_utils.make_gene_variant_dict(proband_ad_im_vars)
        # for gene in proband_all_genes_dict:
        #     print(gene, '->', proband_all_genes_dict[gene])

        proband_genes_multivar = compound_utils.get_gene_dict_multiple_vars(proband_all_genes_dict)
        # for gene in proband_genes_multivar_new:
        #     print(gene, '->', proband_genes_multivar_new[gene])
        
        vars_count_multivar = compound_utils.count_variants_in_dict(proband_genes_multivar)
        log.append_text(
            'Excluding variants in a gene with single variants, {0} variants -> {1} variants'.format(
                str(len(proband_ad_im_vars)), str(vars_count_multivar)))
        print_status('analysisDriver.run_AR_CH() 5_b', None, "")

        # -------- 5.c. only if two parent samples --------
        # exclude variants in genes where that gene in a parent has all proband's variants
        parent_samples = []
        for sample in self.non_proband:
            if sample.family_member_id in PARENTS:
                parent_samples.append(sample)
        
        if len(parent_samples) > 2:
            # continue with result from 5.b. if one or zero parent samples
            uninherited_gene_variants = proband_genes_multivar
        else:
            parents_genes_list = []  # list for each parent's gene-variant dictionary
            for parent in parent_samples:
                genes_dict = compound_utils.make_gene_variant_dict(parent.variants)
                parents_genes_list.append(genes_dict)

            # get proband's genes that DON'T have all its variants in parent's copy of gene
            uninherited_gene_variants = compound_utils.get_gene_unique_vars(
                proband_genes_multivar, parents_genes_list)
            
            vars_count_uninherited = compound_utils.count_variants_in_dict(uninherited_gene_variants)
            log.append_text(
                'Excluding variants with single parent inheritance, {0} variants -> {1} variants'.format(
                    str(vars_count_multivar),
                    str(vars_count_uninherited)))
            print_status('analysisDriver.run_AR_CH() 5_c', None, '')

    # -------- 5.d. exclude genes in ANY unaffected sample --------
        if not self.unaffected: 
            result_variants_dict = uninherited_gene_variants
        else:
            unaffected_nonparent_genes_list = []  # list for unaffected non-parent samples gene-variant dictionaries
            for sample in self.unaffected:
                if sample.family_member_id not in PARENTS:
                    genes_dict = compound_utils.make_gene_variant_dict(sample.variants)
                    unaffected_nonparent_genes_list.append(genes_dict)
            result_variants_dict = compound_utils.get_gene_unique_vars(
                    uninherited_gene_variants, unaffected_nonparent_genes_list)

        vars_count_result = compound_utils.count_variants_in_dict(result_variants_dict)
        log.append_text(
            'Excluding gene if all start positions are in any unaffected members for each gene, '
            '{0} variants -> {1} variants'.format(
                str(vars_count_uninherited), str(vars_count_result)))

        # put variants back into a list
        return compound_utils.variants_dict_to_list(result_variants_dict)


    # ---------------- END ANALYSIS METHODS ----------------

    def assign_samples(self):
        for sample in self.all_samples:
            if sample.family_member_id != FamilyMember.Proband:
                self.non_proband.append(sample)
                if sample.affected_status == AffectedStatus.Affected:
                    self.affected.append(sample)
                elif sample.affected_status == AffectedStatus.Unaffected:
                    self.unaffected.append(sample)
            else:  # proband is on no other list
                self.proband = sample
        debug_log('affected:' + (str(self.affected)))
        debug_log('unaffected:' + (str(self.unaffected)))
        debug_log('non_proband:' + (str(self.non_proband)))
        debug_log('proband:' + str(self.proband))
