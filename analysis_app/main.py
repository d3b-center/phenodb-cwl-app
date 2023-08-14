# -----------------------------------------------------------------------------

# Copyright <2021> <Johns Hopkins School of Medicine>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NON INFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

# -----------------------------------------------------------------------------
#
# DESCRIPTION
#
# THIS SCRIPT PERFORMS VARIANT ANALYSIS FILTERING ACCORDING PHENODB ANALYSIS MODULE
#
# MORE DETAILS MIGHT BE FOUND AT https://mendeliangenomics.org/
#
# Sobreira N, Schiettecatte F, Boehm C, Valle D, Hamosh A. New tools
# for Mendelian disease gene identification: PhenoDB variant analysis
# module; and GeneMatcher, a web-based tool for linking investigators
# with an interest in the same gene. Hum Mutat. 2015 Apr;36(4):425-31.
# doi: 10.1002/humu.22769. PMID: 25684268; PMCID: PMC4820250.
#


import sys
import argparse
from analyzer import Analyzer
from log import Log, print_status
from sample_maker import SampleMaker
from variant_excluder import VariantExcluder
from variant_fields import get_variants_fields, get_header_string
from utils import AnalysisType, PhenoDBException, debug_log


def parse_args(argv):
    parser = argparse.ArgumentParser()
    # samples are CWL 'Record' objects, and each sample has four fields as args
    parser.add_argument('-samples_relation', dest = 'samples_relation', action='append', nargs = '+', required = True)
    parser.add_argument('-samples_sex', dest = 'samples_sex', action='append', nargs = '+', required = True)
    parser.add_argument('-samples_affected', dest = 'samples_affected', action='append', nargs = '+', required = True)
    parser.add_argument('-samples_vcf', dest = 'samples_vcf', action='append', nargs = '+', required = True)
    # end samples args
    parser.add_argument('-analyses', dest = 'analyses_strs', nargs = '+', required = True)
    parser.add_argument('-maf_cutoff', dest = 'maf_cutoff_str', required = True)
    parser.add_argument('-refgene_gene_loc', dest = 'refgene_gene_loc', nargs = '+', required = True)
    result = parser.parse_args(argv)
    return result


# returns a list with one tuple for each sample entered by user
# tuple items: (relationship, sex, affected_status, vcf)
def get_samples_tuples(relation_list, sex_list, affected_list, vcf_list):
    samples = []
    samples_count = len(relation_list)
    i = 0
    try:
        while i < samples_count:  # get items out of list of lists
            samples.append( (relation_list[i][0], sex_list[i][0], affected_list[i][0], vcf_list[i][0]) )
            i += 1
    except OSError:
        raise PhenoDBException("Missing attribute for a sample", "")
    return samples


def get_analysis_enums(analysis_strs):
    analyses_enums = []
    for name in analysis_strs:
        analyses_enums.append(AnalysisType.from_string(name))
    return analyses_enums


def get_maf_float(val):
    try:
        return float(val)
    except ValueError:
        raise PhenoDBException("method: maf is not a valid float.", val)


class AnalysesRunner:
    def __init__(self, samples, field_indices, header_string, start_log_text):
        self.analyzer = Analyzer(samples, field_indices)
        self.proband_start_vars_count = len(self.analyzer.proband_vars)
        self.variants_header = header_string
        self.start_log_text = start_log_text

    def run(self, analysis_type):
        log = Log()
        log.append_text(self.start_log_text)  # each analysis makes new log, but always starts with sample maker steps
        final_variants = self.analyzer.analyze_variants(analysis_type, log)

        # append initial and final proband variant counts to log
        log.append_text(
            'Initial proband count = {0} / Final count = {1}'.format(str(self.proband_start_vars_count), str(len(final_variants))))

        # write analysis log and final variants to separate files
        log.print_summary(analysis_type)
        log.write_log(analysis_type)
        log.write_variants(analysis_type, self.variants_header, final_variants)


if __name__ == '__main__':
    result = parse_args(sys.argv[1:])
    debug_log('sys.argv:' + str(sys.argv), init=True)
    debug_log('parse_args result:' + str(result))
    
    samples_tuples = get_samples_tuples(result.samples_relation, result.samples_sex, result.samples_affected, result.samples_vcf)
    analyses_to_run = get_analysis_enums(result.analyses_strs)
    maf_cutoff = get_maf_float(result.maf_cutoff_str)
    refgene_gene_locations = set(result.refgene_gene_loc)
    debug_log('args transformed:' + str(samples_tuples) + str(analyses_to_run) + str(maf_cutoff) + str(refgene_gene_locations))

    # make variant handlers
    # variant_indices is a dictionary, keys are the variant field and values are the index in variant string
    # TODO clean up how get header
    header_string = get_header_string(samples_tuples[0][3])
    field_indices = get_variants_fields(samples_tuples[0][3])  # use vcf file for any sample
    variant_excluder = VariantExcluder(field_indices, maf_cutoff, refgene_gene_locations)
    

    # make samples and add their starting variants of interest
    sample_maker_log = Log()  # initial variant processing steps are added to every analysis log
    sample_maker = SampleMaker(samples_tuples, variant_excluder, sample_maker_log)
    samples = sample_maker.samples
    for sample in samples:
        debug_log(sample)

    # run the analyses entered by the user
    analyses_runner = AnalysesRunner(samples, field_indices, header_string, sample_maker_log.text)
    for analysis in analyses_to_run:
        print_status('main.run()', None, str(analysis))
        try:
            analyses_runner.run(analysis)
        except Exception:
            raise PhenoDBException('Error during main.run() for ' + str(analysis), '')
    print_status('end', None, '')
