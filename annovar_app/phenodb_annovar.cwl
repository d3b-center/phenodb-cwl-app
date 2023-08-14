{
    "class": "CommandLineTool",
    "cwlVersion": "v1.2",
    "$namespaces": {
        "sbg": "https://sevenbridges.com"
    },
    "id": "lvail1/phenodb-dev/annotate-1/27",
    "baseCommand": [
        "python3",
        "/usr/src/phenodb_annovar/main_annovar.py"
    ],
    "inputs": [
        {
            "id": "Samples",
            "type": "File[]",
            "inputBinding": {
                "prefix": "-vcfs",
                "shellQuote": false,
                "position": 0
            },
            "doc": "VCF files to annotate. One VCF for each individual. May be either uncompressed or gz compressed"
        },
        {
            "sbg:toolDefaultValue": "Annovar_Template",
            "sbg:suggestedValue": {
                "class": "File",
                "path": "64bee6596fd33e37091c3938",
                "name": "annovar_template.tar.gz"
            },
            "id": "Annotations",
            "type": "File",
            "inputBinding": {
                "prefix": "-ref_data",
                "shellQuote": false,
                "position": 2
            },
            "doc": "Project's zipped file with Annovar annotation data"
        },
        {
            "id": "Human_Assembly",
            "type": {
                "type": "enum",
                "symbols": [
                    "Hg19",
                    "Hg38"
                ],
                "name": "Human_Assembly"
            },
            "inputBinding": {
                "prefix": "-version",
                "shellQuote": false,
                "position": 1
            },
            "doc": "Human genome reference version",
            "default": null
        }
    ],
    "outputs": [
        {
            "id": "errorFile",
            "type": "File?",
            "outputBinding": {
                "glob": "exception.txt"
            }
        },
        {
            "id": "resultFile",
            "label": "annotated_vcf",
            "type": "File",
            "outputBinding": {
                "glob": "*multianno.txt"
            }
        },
        {
            "id": "debug",
            "type": "File?",
            "outputBinding": {
                "glob": "debug.txt"
            }
        }
    ],
    "doc": "Sample inputs are available in this Project's Files in the folder 'PhenoDB_Sample_Files,' along with a pdf with screenshots of these steps. For assistance, email both phenodb@jhmi.edu and lvail1@jhu.edu\n\n\n#Steps\n1. Begin with individual VCF files from one or more people\n2. Enter your inputs into the app (described below) and turn on Batching\n3. The task may take up to one hour or longer, depending on the size and number of the input files. When completed, there should be one new file for each VCF you entered, with “hg_38_multianno.txt” added to the end of the file's original name\n4. These output files can be analyzed with the PhenoDB Analysis app\n\n---\n\n#App Input Descriptions\n1. __VCF File(s):__ Individual VCF files for all people included in the analysis\n    - This step can be done for multiple families at once\n    - The files can be either .gz compressed, or uncompressed\n    - Set “Batching” to On for the VCFs, and select “Batch by: File.” This helps the process run faster\n2. __Human_Assembly:__ Select either Hg19 or Hg38\n3. __Annotations:__ ANNOVAR reference data to use for the annotation. Select the folder ‘Annovar_Template’ in the project’s Files",
    "label": "PhenoDB ANNOVAR Annotation",
    "requirements": [
        {
            "class": "ShellCommandRequirement"
        },
        {
            "class": "LoadListingRequirement"
        },
        {
            "class": "DockerRequirement",
            "dockerPull": "pgc-images.sbgenomics.com/lvail1/phenodb_annovar:dev"
        },
        {
            "class": "InitialWorkDirRequirement",
            "listing": [
                "$(inputs.vcf)"
            ]
        },
        {
            "class": "InlineJavascriptRequirement"
        }
    ],
    "sbg:projectName": "PhenoDB_dev",
    "sbg:revisionsInfo": [],
    "sbg:image_url": null,
    "sbg:appVersion": [
        "v1.2"
    ],
    "sbg:id": "lvail1/phenodb-dev/annotate-1/27",
    "sbg:revision": 27,
    "sbg:revisionNotes": "Updated path id of Annovar_Template",
    "sbg:modifiedOn": 1691592579,
    "sbg:modifiedBy": "lvail1",
    "sbg:createdOn": 1683229373,
    "sbg:createdBy": "lvail1",
    "sbg:project": "lvail1/phenodb-dev",
    "sbg:sbgMaintained": false,
    "sbg:validationErrors": [],
    "sbg:contributors": [
        "lvail1"
    ],
    "sbg:latestRevision": 27,
    "sbg:publisher": "sbg",
    "sbg:content_hash": "aa772a0541d55ddc9ff6e420f31edd2ae4ff7267eb1065f798b2ffbfe673bfc6c",
    "sbg:workflowLanguage": "CWL"
}