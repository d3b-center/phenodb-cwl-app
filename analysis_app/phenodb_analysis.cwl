{
    "class": "CommandLineTool",
    "cwlVersion": "v1.2",
    "$namespaces": {
        "sbg": "https://sevenbridges.com"
    },
    "id": "lvail1/phenodb-dev/analysis-dev/31",
    "baseCommand": [
        "python",
        "/usr/src/phenodb_analysis/main.py"
    ],
    "inputs": [
        {
            "sbg:suggestedValue": [
                "Autosomal recessive - Compound heterozygous",
                "Autosomal recessive - Homozygous"
            ],
            "id": "Analysis_Types",
            "type": {
                "type": "array",
                "items": {
                    "type": "enum",
                    "name": "Analysis_Types",
                    "symbols": [
                        "Autosomal dominant - New mutation",
                        "Autosomal dominant - Inherited mutation",
                        "Autosomal dominant - Variants",
                        "Autosomal recessive - Compound heterozygous",
                        "Autosomal recessive - Homozygous",
                        "No value"
                    ]
                }
            },
            "inputBinding": {
                "prefix": "-analyses",
                "shellQuote": false,
                "position": 1
            },
            "label": "Analysis Type(s)",
            "doc": "Inheritance types to analyze among the sample(s)",
            "default": [
                "Autosomal recessive - Compound heterozygous",
                "Autosomal recessive - Homozygous"
            ]
        },
        {
            "sbg:suggestedValue": "0.01",
            "id": "MAF_Cutoff",
            "type": {
                "type": "enum",
                "symbols": [
                    "0",
                    "0.005",
                    "0.01",
                    "0.02",
                    "0.03",
                    "0.04",
                    "0.05",
                    "0.10",
                    "0.20",
                    "0.30",
                    "0.4",
                    "0.5",
                    "0.6",
                    "0.7",
                    "0.8",
                    "0.9",
                    "1.0"
                ],
                "name": "MAF_Cutoff"
            },
            "inputBinding": {
                "prefix": "-maf_cutoff",
                "shellQuote": false,
                "position": 2
            },
            "label": "Exclude minor allele frequency greater than:",
            "doc": "Threshold for what minor allele frequencies (MAF) to exclude. Data sources: ",
            "default": "0.01"
        },
        {
            "sbg:suggestedValue": [
                "exonic",
                "exonic;splicing",
                "splicing"
            ],
            "id": "Refgene_Gene_Location",
            "type": {
                "type": "array",
                "items": {
                    "type": "enum",
                    "name": "Refgene_Gene_Location",
                    "symbols": [
                        "UTR3",
                        "UTR5",
                        "UTR5;UTR3",
                        "exonic",
                        "exonic;splicing",
                        "splicing",
                        "intergenic",
                        "intronic",
                        "ncRNA_UTR3",
                        "ncRNA_UTR5",
                        "ncRNA_exonic",
                        "ncRNA_intronic",
                        "ncRNA_splicing",
                        "upstream",
                        "downstream",
                        "upstream;downstream",
                        "synonymous",
                        "frameshift deletion/insertion, nonframeshift deletion/insertion, stopgain, stoploss, exonic;splicing, splicing"
                    ]
                }
            },
            "inputBinding": {
                "prefix": "-refgene_gene_loc",
                "shellQuote": false,
                "position": 3
            },
            "doc": "Include only variants with these Refgene Gene Locations",
            "default": [
                "exonic",
                "exonic;splicing",
                "splicing"
            ]
        },
        {
            "id": "Samples",
            "type": {
                "type": "array",
                "items": {
                    "type": "record",
                    "name": "Samples",
                    "fields": [
                        {
                            "name": "Relationship",
                            "type": {
                                "type": "enum",
                                "symbols": [
                                    "Proband",
                                    "Mother",
                                    "Father",
                                    "Other_Relative"
                                ],
                                "name": "Relationship"
                            },
                            "inputBinding": {
                                "prefix": "-samples_relation",
                                "shellQuote": false,
                                "position": 0
                            },
                            "doc": "Relationship between this sample and the proband"
                        },
                        {
                            "name": "Sex",
                            "type": {
                                "type": "enum",
                                "symbols": [
                                    "Male",
                                    "Female",
                                    "Unknown or not XX/XY"
                                ],
                                "name": "Sex"
                            },
                            "inputBinding": {
                                "prefix": "-samples_sex",
                                "shellQuote": false,
                                "position": 1
                            },
                            "doc": "Sex of the individual sampled"
                        },
                        {
                            "name": "Affected_Status",
                            "type": {
                                "type": "enum",
                                "symbols": [
                                    "Affected",
                                    "Unaffected",
                                    "Unknown"
                                ],
                                "name": "Affected_Status"
                            },
                            "inputBinding": {
                                "prefix": "-samples_affected",
                                "shellQuote": false,
                                "position": 2
                            }
                        },
                        {
                            "name": "VCF",
                            "type": "File",
                            "inputBinding": {
                                "prefix": "-samples_vcf",
                                "shellQuote": false,
                                "position": 3
                            },
                            "doc": "Annotated VCF"
                        }
                    ]
                }
            },
            "inputBinding": {
                "shellQuote": false,
                "position": 0
            },
            "label": "Samples",
            "doc": "VCFs and characteristics of all samples to include in the analysis"
        }
    ],
    "outputs": [
        {
            "id": "final_variants",
            "label": "Analysis result",
            "type": [
                "File",
                {
                    "type": "array",
                    "items": "File"
                }
            ],
            "outputBinding": {
                "glob": "*.tsv"
            }
        },
        {
            "id": "analysis_summary",
            "type": [
                "File",
                {
                    "type": "array",
                    "items": "File"
                }
            ],
            "outputBinding": {
                "glob": "Log_*"
            }
        },
        {
            "id": "exceptions",
            "type": "File?",
            "outputBinding": {
                "glob": "exception.txt"
            }
        },
        {
            "id": "debug",
            "doc": "debugging info",
            "type": "File?",
            "outputBinding": {
                "glob": "debug.txt"
            }
        }
    ],
    "doc": "Step 2 of PhenoDB, this app analyzes variants. A user manual with screenshots of the below steps, the application's source code, Dockerfile, and CWL are available at [https://github.com/d3b-center/phenodb-cwl-app]( https://github.com/d3b-center/phenodb-cwl-app).\n\nFor more information about PhenoDB, please see [https://phenodb.org/about](https://phenodb.org/about). For assistance, please email both phenodb@jhmi.edu and lvail1@jhu.edu.\n\n#Steps\n1. Begin with annotated VCF files generated by the 'PhenoDB ANNOVAR Annotation' app, which end with 'multianno.txt'\n2. Enter your inputs, descriptions below\n3. When complete, there should be two files for each selected analysis type: one ‘Analysis result’ tsv containing the variants of interest for that inheritance pattern, and one ‘Analysis summary’ file describing the filtering of the variants that led to that result\n4. Cavatica has built-in preview for text files, including column sort in the .tsv analysis results. Click on the names of the files, and select “Preview” to view and sort the .tsv files, and “Raw View” for the .txt files. In the .tsv preview, dynamically sort the results by clicking on column headers\n\n---\n\n#App Inputs\n1. __Samples:__ One or more individuals to be analyzed together. Each Sample has four attributes to be entered:\n    - __Affected Status:__ Affected, Unaffected, or Unknown\n    - __Relationship:__ Proband, or relationship to proband (Mother, Father, Other Relative)\n    - __Sex:__ Male, Female, Unknown or not XX/XY\n    - __VCF:__ Individual’s annotated VCF file from the 'PhenoDB ANNOVAR Annotation' app, which ends with 'multianno.txt'\n2. __Analysis Type(s):__ Choose one or more inheritance patterns for the analysis. Descriptions of the inheritance patterns are below. Recommended default: autosomal recessive compound heterozygous and autosomal recessive homozygous\n3. __Exclude minor allele frequency greater than:__ Choose your cutoff point. Data sources are the ExAC, esp6500siv2, 1000g2014oct, and 1000g2015aug databases. Recommended default: 0.01\n4. __RefGene gene location:__ Select one or more to include. Recommended default, three locations: \"exonic\", \"exonic;splicing\", and \"splicing\"\n\n---\n\n#Inheritance Types: Description and Samples Required\n\n###Autosomal Recessive Compound Heterozygous (AR_CH)\n  - Requires: At least proband\n  - Variants in Result: Includes only the heterozygous variants identified in the proband (assumed to be affected); if there is more than one affected family members, the analysis include only the variants that are identified in all affected members; next, the analysis includes only the genes that have more than one variant in the proband but if the same set of variants in a gene is found in one of the parents or in other unaffected family member then this gene (and its variants) is excluded of the analysis (Sobreira et al., 2015)\n\n\n###Autosomal Recessive Homozygous (AR_H)\n  - Requires: At least proband\n  - Variants in Result: Identifies homozygous variants that are shared by all affected individuals and excludes variants that are homozygous in an unaffected individual (Sobreira et al., 2015)\n\n\n###Autosomal Dominant New Mutation (AD_NM)\n  - Requires: Proband and two parents (trio), and neither parent is affected\n  - Variants in Result: Includes heterozygous variants that are identified in the proband but not in the parents (Sobreira et al., 2015)\n\n\n###Autosomal Dominant Inherited Mutation (AD_IM)\n  - Requires: Proband plus at least one affected or unaffected relative, not necessarily a parent\n  - Variants in Result: Retains heterozygous variants that are shared by affected individuals and excludes those found in unaffected individuals. (Sobreira et al., 2015)\n\n###Autosomal Dominant Variant (AD_V)\n  - Requires: Should be used when only one individual is being analyzed. \n  - Variants in Result: Retains heterozygous variants with a minor allele frequency (MAF) less than the threshold selected for the ExAC, esp6500siv2, 1000g2014oct, 1000g2015aug databases (Sobreira et al., 2015)",
    "label": "PhenoDB Analysis",
    "requirements": [
        {
            "class": "ShellCommandRequirement"
        },
        {
            "class": "DockerRequirement",
            "dockerPull": "pgc-images.sbgenomics.com/lvail1/phenodb_analysis:dev"
        }
    ],
    "sbg:projectName": "PhenoDB_dev",
    "sbg:image_url": null,
    "sbg:appVersion": [
        "v1.2"
    ],
    "sbg:id": "lvail1/phenodb-dev/analysis-dev/31",
    "sbg:revision": 31,
    "sbg:revisionNotes": "Suffix spelling corrected",
    "sbg:modifiedOn": 1697735982,
    "sbg:modifiedBy": "lvail1",
    "sbg:createdOn": 1684844515,
    "sbg:createdBy": "lvail1",
    "sbg:project": "lvail1/phenodb-dev",
    "sbg:sbgMaintained": false,
    "sbg:validationErrors": [],
    "sbg:contributors": [
        "lvail1"
    ],
    "sbg:latestRevision": 31,
    "sbg:publisher": "sbg",
    "sbg:content_hash": "a452eedaec90d5cc012b9703bc961d6acae225d7912ef5958eebd5abb8518ad53",
    "sbg:workflowLanguage": "CWL"
}