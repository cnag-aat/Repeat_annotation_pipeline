#!/usr/bin/env python3
import os
import json
import argparse
import sys

#Author: Jessica Gomez, CNAG-CRG.
#Contact email: jessica.gomez@cnag.crg.eu
#Date:20190524

class CreateConfigurationFile(object):
    """Class which manages Configuration file Manager"""
      
    def __init__(self):
        """Class constructor"""
        #GENERAL PARAMETERS
        self.configFile = "Repeat_annotation.config"                               #Name of the json configuration file with the pipeline parameters to be created
        self.species_database = "None"                                             #Existant database to run a first time Repeat Masker
        self.rmaskCores = 8                                                        #Number of threads to run RepeatMasker
        self.projectName = None                                                    #Repeat Modeler database to be created
        self.blastdb = "/scratch/project/devel/aateam/blastdbs/swissprot"          #Blast database to check presence of protein families in RepeatModeler library
        self.rmodCores= 2	
        self.Recover_Rmod = None                                                   #Directory to recover RMod
        self.blastCores = 4
        self.logs_dir = "logs"                                                     #Directory to keep all the log files
        self.repeat_library = None                                                 #fasta file containing a pre-existant library of repeats 
        self.RMOD_mode = "False"                                                   #Variable to define if Repeat Modeler should be run
        
        #INPUT PARAMETERS
        self.genome = None                                                         #Genome to mask

        #OUTPUT PARAMETERS
        self.blastout = "None"                                                     #File to keep the blast results

###
        #DICTIONARIES
        self.allParameters = {}
        self.generalParameters = {}
        self.inputParameters = {}
        self.outputParameters = {}

####

    def register_parameter(self, parser):
        """Register all parameters with the given
        argparse parser"""
        self.register_general(parser)
        self.register_input(parser)
        self.register_output(parser)

###

    def register_general(self, parser):
        """Register all general parameters with the given
        argparse parser

        parser -- the argparse parser
        """
        general_group = parser.add_argument_group('General Parameters')
        general_group.add_argument('--configFile', dest="configFile", metavar="configFile", default='Repeat_annotation.config', help='Configuration file with the pipeline parameters to be created. Default %s' % self.configFile)
        general_group.add_argument('--projectName', dest="projectName", metavar="projectName", help='Repeat Modeler database to be created. Default %s' % self.projectName)
        general_group.add_argument('--species-database', dest="species_database", metavar="species_database", help='Existant database to run a first time Repeat Masker. Default %s' % self.species_database)
        general_group.add_argument('--blastdb', dest="blastdb", metavar="blastdb", default= '/project/devel/aateam/blastdbs/swissprot', help='Blast database to check presence of protein families in RepeatModeler library. Default %s' % self.blastdb)
        general_group.add_argument('--blast-cores', dest="blastCores", metavar="blastCores", type=int, default=self.blastCores, help='Default %s' % self.blastCores)
        general_group.add_argument('--rmask-cores', dest="rmaskCores", metavar="rmaskCores", type=int, default=self.rmaskCores, help='Default %s' % self.rmaskCores)
        general_group.add_argument('--rmod-cores', dest="rmodCores", metavar="rmodCores", type=int, default=self.rmodCores, help='Default %s' % self.rmodCores)
        general_group.add_argument('--rmod-dir', dest="Recover_Rmod", metavar="Recover_Rmod", default=self.Recover_Rmod, help='Default %s' % self.Recover_Rmod)
        general_group.add_argument('--logs-dir', dest="logs_dir", metavar="logs_dir", help='Directory to keep all the log files. Default %s' % self.logs_dir)
        general_group.add_argument('--repeat-library', dest="repeat_library", metavar="repeat_library", help='fasta file containing a pre-existant library of repeats. Default %s' % self.repeat_library)
        general_group.add_argument('--RMOD-mode', dest="RMOD_mode",action="store_true", help='If specified, Repeat Modeler will be run')        


    def register_input(self, parser):
        """Register all input parameters with the given
        argparse parser

        parser -- the argparse parser
        """
        input_group = parser.add_argument_group('Inputs')
        input_group.add_argument('--genome', dest="genome", metavar="genome", help='Path to the fasta genome. Default %s' % self.genome)

    def register_output(self, parser):
        """Register all output parameters with the given
        argparse parser

        parser -- the argparse parser
        """
        output_group = parser.add_argument_group('Outputs')
        output_group.add_argument('--blastout', dest="blastout", metavar="blastout", help='File to keep the blast results. Default %s' % self.blastout)

####

    def check_parameters(self,args):
        """Check parameters consistency
            
        args -- set of parsed arguments"""

        working_dir = os.getcwd() + "/"

        if args.genome == None:
            print ("Sorry! No genome fasta file defined")
            parser.print_help()
            sys.exit(-1)
        else:
            args.genome = working_dir + os.path.basename(args.genome) 
            if not os.path.exists(args.genome):
                print (args.genome + " not found" )
           
        if args.logs_dir:
            args.logs_dir = os.path.abspath(args.logs_dir) + "/"
        else:
            args.logs_dir = working_dir + self.logs_dir + "/"

     #   if args.projectName==None:
      #      print "Sorry! No project name given"
      #  else:
            if args.blastout:
                self.blastout = args.blastout
            elif args.projectName!=None:
                args.blastout = args.projectName + "-families.BLAST.sprot.out"
            elif args.Recover_Rmod or args.RMOD_mode == True:
                print ("Sorry! No project name given")

        if args.Recover_Rmod:
            args.Recover_Rmod = os.path.abspath(args.Recover_Rmod)

        if args.repeat_library:
            args.repeat_library = os.path.abspath(args.repeat_library) 	

###

    def storeGeneralParameters(self,args):
        """Updates general parameters to the map of parameters to be store in a JSON file

        args -- set of parsed arguments
        """
        self.generalParameters["projectName"] = args.projectName
        self.generalParameters["logs_dir"] = args.logs_dir
        self.generalParameters["species_database"] = args.species_database
        self.generalParameters["blastdb"] = args.blastdb
        self.generalParameters["blastCores"] = args.blastCores
        self.generalParameters["rmaskCores"] = args.rmaskCores
        self.generalParameters["rmodCores"] = args.rmodCores
        self.generalParameters["Recover_Rmod"] = args.Recover_Rmod
        self.generalParameters["Repeat_library"] = args.repeat_library
        self.generalParameters["RMOD_mode"]= args.RMOD_mode
        self.allParameters  ["Parameters"] = self.generalParameters

    def storeInputParameters(self,args):
        """Updates input parameters to the map of parameters to be store in a JSON file

        args -- set of parsed arguments
        """
        self.inputParameters["genome"] = args.genome
        self.allParameters ["Inputs"] = self.inputParameters

    def storeOutputParameters(self,args):
        """Updates output parameters to the map of parameters to be store in a JSON file

        args -- set of parsed arguments
        """
        self.outputParameters["blast_out"] = args.blastout
        self.allParameters ["Outputs"] = self.outputParameters


#####

#1.Create object class Configuration File
configManager = CreateConfigurationFile()

#2.Create object for argument parsinng
parser = argparse.ArgumentParser(prog="create_configuration_file",
                description="Create a configuration json file for the repeat annotation pipeline."
                )     

#2.1 Updates arguments and parsing
configManager.register_parameter(parser)

args = parser.parse_args()

#2.2 Check Parameters
configManager.check_parameters(args)

#3. store arguments to super map structure
configManager.storeGeneralParameters(args)
configManager.storeInputParameters(args)
configManager.storeOutputParameters(args)


###

#4. Store JSON file
with open(args.configFile, 'w') as of:
    json.dump(configManager.allParameters, of, indent=2)




