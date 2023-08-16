# PhenoDB CWL App

This repository contains user instructions, sample data, and source code for
the version of the PhenoDB application hosted on Cavatica.

For more information about PhenoDB, please go to https://phenodb.org/about.


### Repo Description

The PhenoDB workflow is done in two independent steps that are each a
separate code base and app on Cavatica. The first step is Annovar annotation, 
and the second step is variant analysis.

PhenoDB_Cavatica_User_Guide.pdf: instructions with screenshots of how to use the two apps

example_inputs_results: example input files to run in the applications, and example results
of an analysis

annovar_app: Dockerfile, CWL and python files for first step's app

analysis_app: Dockerfile, CWL and python files for second step's app