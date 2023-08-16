from log import Log, print_status
from utils import FamilyMember, AffectedStatus, Sex, PhenoDBException


# makes a Sample object with variants from user inputs
class SampleMaker:
    def __init__(self, samples_tuples, variant_excluder, sample_maker_log):
        self.sample_maker_log = sample_maker_log
        self.variant_excluder = variant_excluder
        self.samples = self.generate_samples(samples_tuples)
        

    # samples_tuples: a list with one tuple for each sample entered by user
    def generate_samples(self, sample_tuples):
        samples = []
        for sample_attribute in sample_tuples:
            # tuple items: (relationship, sex, affected_status, vcf_file_path)
            family_member_id = FamilyMember.from_string(sample_attribute[0])
            sex = Sex.from_string(sample_attribute[1])
            affected = AffectedStatus.from_string(sample_attribute[2])
            variants = self.get_variants(sample_attribute[3], family_member_id == FamilyMember.Proband)
            new_sample = Sample(family_member_id, sex, affected, variants)
            samples.append(new_sample)
        return samples
    

    # get variants for sample; only proband's variant filtering added to analysis log
    def get_variants(self, vcf_file_path, is_proband):
        all_variants = get_all_variants(vcf_file_path)
        if is_proband:
            return self.variant_excluder.filter(all_variants, self.sample_maker_log)
        else:
           return self.variant_excluder.filter(all_variants, Log())  # pass throwaway log
    

class Sample:
    def __init__(self, family_member_id, sex, affected_status, variants):
        self.family_member_id = family_member_id
        self.sex = sex
        self.affected_status = affected_status
        self.variants = variants

    def __str__(self):
        return f'Sample({self.family_member_id}, {self.sex}, {self.affected_status}, variants_count={len(self.variants)})'


# returns a list of strings that are the sample's vcf
# each variant is a line in the vcf
def get_all_variants(vcf_file_path):
    try:
        with open(vcf_file_path, 'r') as reader:
            variants = []
            i = 0
            for line in reader.readlines():
                i += 1
                if line[0] != "#" and not line.startswith('Chromosome'):
                    variants.append(line[:-1])
            print_status('sample.find_variants()', i, '')
            return variants
    except:
        raise PhenoDBException('File not found:', vcf_file_path)
