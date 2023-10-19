import argparse
import gzip
import os
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from pytz import timezone
from subprocess import PIPE
from utils import run_command, AnnovarException


def main(vcf_files, version_name, ref_data_tar):
    # no second arg or True for container; False for local test run
    annovar_dir_path = get_paths()
    ref_data_dir = extract(ref_data_tar)
    print_dir_contents([annovar_dir_path, ref_data_dir])

    # convert then annotate each VCF
    for vcf in vcf_files:
        debug_log('in loop for vcf: ' + vcf)
        if vcf.endswith('.gz'):
            vcf = uncompress(vcf)
        
        # convert vcf to Annovar format, and write to a new file with suffix 'avinput'
        vcf_converted = os.path.basename(vcf[:-3] + 'avinput')
        write_conversion(vcf, vcf_converted, annovar_dir_path)
        
        # annotate the converted file with Annovar reference data
        try:
            write_annotation(vcf_converted, version_name, annovar_dir_path, ref_data_dir)
        except Exception as ex:
            raise AnnovarException('Converted VCF could not be annotated:' + vcf_converted, ex)


def get_paths(container=True):
    if container:  
        prefix = '/usr/src/phenodb_annovar/'  # production paths in container
    else:  
        prefix = './'  # paths to run as a script on local machine
    return prefix + 'annovar/'


def print_dir_contents(directories):
    for direct in directories:
        debug_log('Contents of directory: ' + direct)
        for path in Path(direct).rglob('*'):
            debug_log('    ' + str(path))

    
def extract(ref_data_filename):
    debug_log('in extract()')
    cmd_extract = ['tar -xvf ' + ref_data_filename]
    debug_log('cmd_extract: ' + ' '.join(cmd_extract))
    result = subprocess.run(cmd_extract, shell=True, stderr=PIPE)
    if result.returncode != 0:
        str_err = result.stderr.decode('utf-8')
        raise AnnovarException('Reference data could not be extracted from ' + ref_data_filename + ', error_string: ' + str_err, '')
    else:
        return os.path.basename(ref_data_filename[:-7])  # dir is path without '.tar.gz' from end


def uncompress(file_in):
    debug_log('in uncompress()')
    try:
        with gzip.open(file_in, 'rb') as f_in:
            file_out = os.path.basename(file_in[:-3])  # # remove '.gz' for out file name
            with open(file_out, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
                return file_out
    except Exception as ex:
        raise AnnovarException('File could not be uncompressed: ' + file_in, ex)


# writes converted file to working directory
def write_conversion(vcf, vcf_converted, annovar_dir_path):
    cmd_convert = ['perl', annovar_dir_path + 'convert2annovar.pl', '--format', 'vcf4', '--includeinfo', '--withzyg', '--outfile', vcf_converted, vcf]
    debug_log('cmd_convert: ' + ' '.join(cmd_convert))
    result = subprocess.run(cmd_convert, stderr=PIPE)
    if result.returncode != 0:
        str_err = result.stderr.decode('utf-8')
        raise AnnovarException('VCF could not be converted: ' + vcf + ', error_string: ' + str_err, '')


# writes output to working directory
# suffix automatically added by annovar is eg 'hg38_multianno.txt'
# smaller values for faster test runs:
    # data_sources = 'refGene,ensGene'
    # ops = 'g,g'
def write_annotation(vcf_converted, version_name, annovar_dir_path, ref_data_dir):
    debug_log('in write_annotation()')
    out_name = vcf_converted[:-8]  # remove '.avinput' file extension
    data_sources = 'refGene,ensGene,esp6500siv2_all,esp6500siv2_aa,esp6500siv2_ea,1000g2014oct_all,1000g2014oct_afr,1000g2014oct_amr,1000g2014oct_eas,1000g2014oct_eur,1000g2014oct_sas,1000g2015aug_all,1000g2015aug_afr,1000g2015aug_amr,1000g2015aug_eas,1000g2015aug_eur,1000g2015aug_sas,avsnp142,avsnp144,avsnp147,avsnp150,exac03'
    ops = 'g,g,f,f,f,f,f,f,f,f,f,f,f,f,f,f,f,f,f,f,f,f'

    if version_name == 'Hg19':
        version = 'hg19'
    elif version_name == 'Hg38':
        version = 'hg38'
    else:
        raise AnnovarException('Invalid human assembly version: ' + version_name, '')

    cmd_annotate = ['perl', annovar_dir_path + 'table_annovar.pl', '-buildver', version, '-otherinfo', '-remove', '-protocol', data_sources, '-operation', ops, '--outfile', out_name, vcf_converted, ref_data_dir]
    debug_log('cmd_annotate: ' + ' '.join(cmd_annotate))
    result = subprocess.run(cmd_annotate, stderr=PIPE)
    if result.returncode != 0:
        str_err = result.stderr.decode('utf-8')
        raise AnnovarException('Converted VCF could not be annotated: ' + vcf_converted + ', error_string: ' + str_err, '')


def debug_log(message, init=False):
    if init:
        mode = 'w'
    else:
        mode = 'a'
    with open('debug.txt', mode) as f:
        f.write(str(message) + '\n')


def parse_args(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('-vcfs', dest = 'vcfs', nargs = '+', required = True)
    parser.add_argument('-version', dest = 'version', required = True)
    parser.add_argument('-ref_data', dest = 'refData', required = True)
    result = parser.parse_args(argv)
    return result


if __name__ == '__main__':
    result = parse_args(sys.argv[1:])
    debug_log('sys.argv:' + str(sys.argv), init=True)
    debug_log('\n' + str(result))
    ref_data_tar = result.refData
    vcfs = result.vcfs
    version = result.version
    main(vcfs, version, ref_data_tar)