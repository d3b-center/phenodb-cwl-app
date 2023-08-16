import traceback
from enum import Enum

class PhenoDBException(Exception):
    def __init__(self, exception_string, exception_object):
        outFile = open("exception.txt", "w")
        outFile.write("exception_string:\n"+exception_string)
        outFile.write("\n\n\nexception_object:\n"+str(exception_object))
        outFile.write("\n\n\nTraceback:\n"+"\n".join(traceback.format_stack()))
        outFile.close()
        super().__init__(exception_string, exception_object)


class AnalysisType(Enum):
    AR_CH = 'Autosomal recessive - Compound heterozygous'
    AR_H = 'Autosomal recessive - Homozygous'
    AD_NM = 'Autosomal dominant - New mutation'
    AD_IM = 'Autosomal dominant - Inherited mutation'
    AD_V = 'Autosomal dominant - Variants'

    @classmethod
    def from_string(cls, string):
        for member in cls.__members__.values():
            if member.value == string:
                return member
        raise ValueError(f"Invalid analysis type: '{string}'")


class AffectedStatus(Enum):
    Affected = 'Affected'
    Unaffected = 'Unaffected'
    Other = 'Other'

    @classmethod
    def from_string(cls, string):
        for member in cls.__members__.values():
            if member.value == string:
                return member
        else:
            return AffectedStatus.Other


class FamilyMember(Enum):
    Proband = 'Proband'
    Mother = 'Mother'
    Father = 'Father'
    Other = 'Other'

    @classmethod
    def from_string(cls, string):
        for member in cls.__members__.values():
            if member.value == string:
                return member
        else:
            return FamilyMember.Other


class Sex(Enum):
    Female = 'Female'
    Male = 'Male'
    Other = 'Other'

    @classmethod
    def from_string(cls, string):
        for member in cls.__members__.values():
            if member.value == string:
                return member
        else:
            return Sex.Other

      
def debug_log(message, init=False):
    if init:
        mode = 'w'
    else:
        mode = 'a'
    with open('debug.txt', mode) as f:
        f.write('\n' + str(message) + '\n')


# helper method for VariantField
def matches_maf(string):
    #print('checking string:', string)
    if string.startswith(VariantField.MAF.value):
        #print('matched MAF')
        return True
    else:
        #print('did not match MAF')
        return False


class VariantField(Enum):
    CHR = ['Chromosome', 'Chr']
    START = ['StartPosition', 'Start']
    END = ['EndPosition', 'End']
    REF = ['ReferenceAllele', 'Ref']
    ALT = ['AlternativeAllele', 'Alt']
    GT = ['Otherinfo1', 'Genotype', 'GT']
    REF_GENE_LOC = ['Func.refGene', 'RefgeneGeneLocation']
    REF_GENE_NAME = ['Gene.refGene', 'RefgeneGeneName']
    REF_GENE_EXON_FUNC = ['ExonicFunc.refGene', 'RefgeneExonFunction']
    MAF = ('ExAC_', 'esp6500siv2_', '1000g2014oct_', '1000g2015aug_')  # allows incomplete matches

    @classmethod
    def from_string(cls, string):
        for member in cls.__members__.values():
            if string in member.value:
                return member
        if (matches_maf(string)):
            return VariantField.MAF