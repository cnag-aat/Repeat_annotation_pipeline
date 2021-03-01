# Repeat_annotation_pipeline
Pipeline used in the CNAG AATEAM to annotate repeats in genome assemblies

1. Create the config file with create_config_files_repeats.py:
```bash
create_config_files_repeats.py -h
usage: create_configuration_file [-h] [--configFile configFile]
                                 [--projectName projectName]
                                 [--species-database species_database]
                                 [--blastdb blastdb]
                                 [--blast-cores blastCores]
                                 [--rmask-cores rmaskCores]
                                 [--rmod-cores rmodCores]
                                 [--rmod-dir Recover_Rmod]
                                 [--logs-dir logs_dir]
                                 [--repeat-library repeat_library]
                                 [--RMOD-mode] [--genome genome]
                                 [--blastout blastout]

Create a configuration json file for the repeat annotation pipeline.

optional arguments:
  -h, --help            show this help message and exit

General Parameters:
  --configFile configFile
                        Configuration file with the pipeline parameters to be
                        created. Default Repeat_annotation.config
  --projectName projectName
                        Repeat Modeler database to be created. Default None
  --species-database species_database
                        Existant database to run a first time Repeat Masker.
                        Default None
  --blastdb blastdb     Blast database to check presence of protein families
                        in RepeatModeler library. Default
                        /scratch/project/devel/aateam/blastdbs/swissprot
  --blast-cores blastCores
                        Default 4
  --rmask-cores rmaskCores
                        Default 8
  --rmod-cores rmodCores
                        Default 2
  --rmod-dir Recover_Rmod
                        Default None
  --logs-dir logs_dir   Directory to keep all the log files. Default logs
  --repeat-library repeat_library
                        fasta file containing a pre-existant library of
                        repeats. Default None
  --RMOD-mode           If specified, Repeat Modeler will be run

Inputs:
  --genome genome       Path to the fasta genome. Default None

Outputs:
  --blastout blastout   File to keep the blast results. Default None

```
2. Personalize the specification file for your run
3. Launch the Snakemake pipeline:
```bash
snakemake --notemp -j 999 --snakefile RepeatAnnotation.Snakefile --is {target_file} --cluster "python3 /project/devel/aateam/src/Snakemake-CNAG/sbatch-cnag.py {dependencies}" --configfile Repeat_annotation.config  --cluster-config RepeatAnnotation.spec -np
```
np is needed to make a dry-run, remove it when you're ready to launch the pipeline
{target_file} is the final output file that you want the pipeline to produce
