{
    "class": "CommandLineTool",
    "cwlVersion": "v1.2",
    "$namespaces": {
        "sbg": "https://sevenbridges.com"
    },
    "id": "lvail1/phenodb-dev/annotate-1/46",
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
            "sbg:suggestedValue": {
                "class": "File",
                "path": "652d747266f28c0a49bcd72d",
                "name": "annovar_template.tar.gz"
            },
            "id": "Annotations",
            "type": "File",
            "inputBinding": {
                "prefix": "-ref_data",
                "shellQuote": false,
                "position": 2
            },
            "doc": "Provided tar.gz with ANNOVAR annotation data"
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
            "doc": "File with debugging info",
            "type": "File?",
            "outputBinding": {
                "glob": "debug.txt"
            }
        }
    ],
    "doc": "Step 1 of PhenoDB, this app annotates VCF files with ANNOVAR. A user manual with screenshots of the below steps, the application's source code, Dockerfile, and CWL are available at [https://github.com/d3b-center/phenodb-cwl-app]( https://github.com/d3b-center/phenodb-cwl-app).\n\nFor more information about PhenoDB, please see [https://phenodb.org/about](https://phenodb.org/about). For assistance, please email both phenodb@jhmi.edu and lvail1@jhu.edu.\n\n\n#Steps\n1. Begin with one or more individual VCF files. Any VCF files can be annotated together, but only related individuals should be analyzed together in the next step\n2. Enter your inputs (described below) and turn on Batching\n3. The task may take up to one hour or longer to complete, depending on the size and number of VCFs. When completed, there should be one new file for each VCF you entered, with “hg_38_multianno.txt” added to the end of the file's original name\n4. These output files can be analyzed with the PhenoDB Analysis app\n\n---\n\n#App Input Descriptions\n1. __VCF File(s):__ Individual VCF files for analysis\n    - The files can be either .gz compressed, or uncompressed\n    - Set “Batching” to On for the VCFs, and select “Batch by: File.” This helps the process run faster\n2. __Human_Assembly:__ Select either Hg19 or Hg38\n3. __Annotations:__ ANNOVAR reference data to use for the annotation. This should be automatically filled with \"annotation_template.tar.gz\" when you run the app. See the instructions about copying the Cavatica app for how to include this file",
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
            "dockerPull": "pgc-images.sbgenomics.com/lvail1/phenodb_annovar:8"
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
    "sbg:image_url": null,
    "sbg:appVersion": [
        "v1.2"
    ],
    "sbg:id": "lvail1/phenodb-dev/annotate-1/46",
    "sbg:revision": 46,
    "sbg:revisionNotes": "Instructions updated",
    "sbg:modifiedOn": 1697723344,
    "sbg:modifiedBy": "lvail1",
    "sbg:createdOn": 1683229373,
    "sbg:createdBy": "lvail1",
    "sbg:project": "lvail1/phenodb-dev",
    "sbg:sbgMaintained": false,
    "sbg:validationErrors": [],
    "sbg:contributors": [
        "lvail1"
    ],
    "sbg:latestRevision": 46,
    "sbg:publisher": "sbg",
    "sbg:content_hash": "a88542f54397f9c22d5d48fa1a886521aa91cb17988da0dfe909badf11964e36a",
    "sbg:workflowLanguage": "CWL"
}