shell.prefix("source ~jgomez/init_shell")

from datetime import datetime

date = datetime.now().strftime('%Y%m%d.%H%M%S')

logs_dir = config["Parameters"]["logs_dir"]
if not os.path.exists(logs_dir):
    os.makedirs(logs_dir)
name = os.path.basename(config["Inputs"]["genome"])

if config["Parameters"]["species_database"]:
  rule Repeat_Masker_prev:
    input: 
      genome = config["Inputs"]["genome"]
    output:
      masked = config["Inputs"]["genome"] + ".first_masked"
    params:
      species = config["Parameters"]["species_database"]
    log:
      logs_dir + str(date) + ".rmask1.out"
    threads: config["Parameters"]["rmaskCores"]
    shell:
      "module unload intel;"
      "/apps/REPEATMASKER/4.0.7/RepeatMasker -nolow -gff -pa {threads} -species {params.species} {input.genome};"
      "mv {input.genome}.masked {output.masked};"

  premasked = rules.Repeat_Masker_prev.output.masked

elif config["Parameters"]["Repeat_library"]:
  rule Repeat_Masker_prev:
    input: 
      genome = config["Inputs"]["genome"],
      library = config["Parameters"]["Repeat_library"]
    output:
      masked = config["Inputs"]["genome"] + ".first_masked"
    params:

    log:
      logs_dir + str(date) + ".rmask1.out"
    threads: config["Parameters"]["rmaskCores"]
    shell:
      "module unload intel;"
      "/apps/REPEATMASKER/4.0.7/RepeatMasker -nolow -gff -pa {threads} -lib {input.library} {input.genome};"
      "mv {input.genome}.masked {output.masked};"

  premasked = rules.Repeat_Masker_prev.output.masked

else:
  premasked = config["Inputs"]["genome"]

if config["Parameters"]["Recover_Rmod"]:
  rule Repeat_Modeler:
    input:
      genome = premasked
    output:
      lib = config["Parameters"]["projectName"] + "-families.fa"
    params:
      database = config["Parameters"]["projectName"],
      recover = config["Parameters"]["Recover_Rmod"]
    threads: config["Parameters"]["rmodCores"]
    log:
      logs_dir + str(date) + ".rmod.out"
    shell:
      "module purge; module unload intel; module load perl; module load REPEATMODELER/1.0.11;"
      "RepeatModeler -recoverDir {params.recover} -pa {threads} -database {params.database} "

elif config["Parameters"]["RMOD_mode"]:
  rule Repeat_Modeler:
    input:
      genome = premasked
    output:
      lib = config["Parameters"]["projectName"] + "-families.fa"
    params:
      database = config["Parameters"]["projectName"]
    threads: config["Parameters"]["rmodCores"]
    log:
      logs_dir + str(date) + ".rmod.out"
    shell:
      "module purge; module unload intel; module load perl; module load REPEATMODELER/1.0.11;"
      "BuildDatabase -engine ncbi -name {params.database} {input.genome};"
      "RepeatModeler -pa {threads} -database {params.database}"

if config["Parameters"]["Recover_Rmod"] or config["Parameters"]["RMOD_mode"]:
  rule Filter_lib:
    input: 
      genome= premasked,
      lib=rules.Repeat_Modeler.output.lib
    output:
      blast = config["Outputs"]["blast_out"],
      filtered = rules.Repeat_Modeler.output.lib + ".noproteins.fa"
    params:
      blastdb = config["Parameters"]["blastdb"],
    threads: config["Parameters"]["blastCores"]
    log: logs_dir + str(date) + ".filter.out"
    shell:
      "runBlastp.jip -q {input.lib} -d {params.blastdb} -o {output.blast} -t {threads}; "
      "cat {output.blast} | cut -f 1 | sort | uniq > protein_hits.ids;"
      "filter_fasta_from_ids.pl -f {input.lib} -l protein_hits.ids -b > {output.filtered};"

  rule Repeat_Masker_final:
    input: 
      genome= premasked,
      lib=rules.Filter_lib.output.filtered
    output:
      config["Inputs"]["genome"] + ".masked"
    log:
      logs_dir + str(date) + ".rmask2.out"
    threads: config["Parameters"]["rmaskCores"]
    shell:
      "module unload intel;"
      "/apps/REPEATMASKER/4.0.7/RepeatMasker -nolow -gff -pa {threads} -lib {input.lib} {input.genome};"
      "mv {input.genome}.masked {output}" 

