from utils import VariantField

class CompoundAnalyzerUtils(object):
    def __init__(self, analysis_utils):
        self.analysis_utils = analysis_utils


    # returns a ditionary where keys are gene_name, and values are sets of the gene's unformatted variants
    # note: adding cars formatted makes test dictionry printouts readable
    def make_gene_variant_dict(self, variants):
        gene_variants_dict = {}
        for var in variants:
            # formatted_var = self.analysis_utils.format_variant(var)
            gene_name = var.split("\t")[self.analysis_utils.field_indices[VariantField.REF_GENE_NAME]]
            if gene_name in gene_variants_dict:
                gene_variants_dict[gene_name].add(var)
            else:
                gene_variants_dict[gene_name] = {var}
        return gene_variants_dict


    # return gene-variants dictionary with only genes with more than 1 variant
    def get_gene_dict_multiple_vars(self, gene_variants_dict):
        # self.test_print_dict(gene_variants_dict)
        multivar_genes = {}
        for gene in gene_variants_dict:
            if len(gene_variants_dict[gene]) > 1:
                multivar_genes[gene] = gene_variants_dict[gene]
        # self.test_print_dict(multivar_genes)
        return multivar_genes
    
    
    # TODO make test case for this
    # return genes from genes_to_check for which ALL of its of variants
    #     are NOT found in the values for that gene in another dict
    # example: 
    #     genes_to_check has this gene:  geneA -> (var1, var2, var3)
    #     other_gene_dicts can have that gene, or not
    #         other_gene_dicts[1]    geneA -> (var2, var3)
    #         other_gene_dicts[2]    [does not have geneA]
    #         other_gene_dicts[3]    geneA -> (var1, var4, var5)
    # geneA INCLUDED in return value because all its variants are NOT in another dictionary
    def get_gene_unique_vars(self, genes_dict_to_check, other_gene_dicts):
        if not other_gene_dicts:
            return genes_dict_to_check
        else:
            unique_gene_variants = {}
            for gene_name in genes_dict_to_check:
                gene_vars_unique = True
                for other_gene_dict in other_gene_dicts:
                    if gene_name in other_gene_dict:
                        if genes_dict_to_check[gene_name].issubset(other_gene_dict[gene_name]):
                            gene_vars_unique = False
                            break
                if gene_vars_unique:
                    unique_gene_variants[gene_name] = genes_dict_to_check[gene_name]
            return unique_gene_variants
                    

    # returns the number of variants (keys) in a gene-variant dictionary
    def count_variants_in_dict(self, gene_variant_dict):
        variants_count = 0
        for gene_name in gene_variant_dict:
            variants_count += len(gene_variant_dict[gene_name])
        return variants_count


    # returns a list of all variants in the dictionary (vars are keys in the dict)
    def variants_dict_to_list(self, genes_variants_dict):
        variants = set()
        [variants.update(var) for var in genes_variants_dict.values()]
        return list(variants)
    
    
    def test_print_dict(self, gene_variants_dict):
        print('\nCount of genes:', str(len(gene_variants_dict)))
        print('Count of variants:', str(self.count_variants_in_dict(gene_variants_dict)))
        print('---- All items in dictionary ----')
        for gene in gene_variants_dict:
            print(gene, '->', gene_variants_dict[gene])
