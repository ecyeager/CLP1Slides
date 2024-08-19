#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Elyse Yeager, Andrew Rechnitzer, Joel Feldman"
__copyright__ = "Copyright (C) 2021 Elyse Yeager, Andrew Rechnitzer, and Joel Feldman"
__credits__ = ["Elyse Yeager, Andrew Rechnitzer"]
__license__ = "GPL-3.0-or-later"

#################################################################
# PYTHON MODULE IMPORTS - do not change
#################################################################

from glob import glob
import os
import subprocess
import shutil


#################################################################
# DEBUG
#################################################################
# Set the following to True to see what files will be generated
# without generating them
dry_run = False

#################################################################
# COMPILATION CHOICES
#################################################################
## There are three versions possible for each file: beamer, handout, and prep. 
## To choose which to print, set the following to True or False:

print_beamer=True
print_handout=True
print_prep=True

## There are two collections of files: single sections, 
## sections grouped into weeks
## There are also miscellaneous files: StudentWorkbook, Review, and ReadMe
## To choose which to print, set the following to True or False:

print_sections=True
print_weeks=True
print_readme=True
print_review=True
print_studentworkbook=True



#################################################################
## LISTS OF SECTIONS AND WEEKS
#################################################################
## If you would like to omit some weeks or sections from the list of 
## files to compile, then
## comment out the corresponding lines in the lists below.
## If print_sections is set to 0, all sections will be omitted whether or not
## they are in the list.
## If print_weeks is set to 0, all weeks will be omitted whether or not
## they are in the list.

#section number, section name
section_names_list = [
    ["1_1","Tangent"],
    ["1_2","Velocity"],
    ["1_3","LimitOfFunction"],
    ["1_4","LimitLaws"],
    ["1_5","LimitsAtInfinity"],
    ["1_6","Continuity"],
    ["1_7","LimitsFormal"],
    ["1_8","FormalLimitsInfinity"],
    ["2_1","RevisitingTangent"],
    ["2_2","DefOfDerivative"],
    ["2_3","InterpOfDeriv"],
    ["2_4","ArithmeticOfDeriv"],
    ["2_7","DerivOfExponential"],
    ["2_8","DerivOfTrig"],
    ["2_9","ChainRule"],
    ["2_10","Logarithm"],
    ["2_11","Implicit"],
    ["2_12","InverseTrig"],
    ["2_13","MeanValueThm"],
    ["2_14","HigherDerivs"],
    ["3_1","VelocityAcceleration"],
    ["3_2","RelatedRates"],
    ["3_3","ExponentialGrowth"],
    ["3_4","TaylorPolynomials"],
    ["3_5","Optimisation"],
    ["3_6","Sketching"],
    ["3_7","LHopital"],
    ["4_1","Antiderivatives"],
]


#weeknumber,weekname,sectionnumbers
week_list = [
    ["1","Limits",["1_1","1_2","1_3","1_4"]],
    ["2","Limits",["1_5","1_6","2_1","2_2","2_3"]],
    ["3","Derivs",["2_4","2_7"]],
    ["4","Derivs",["2_8","2_9"]],
    ["5","Implicit",["2_10","2_11","2_12"]],
    ["6","RatesOfChange",["2_13","2_14","3_1","3_2"]],
    ["7","TaylorPolynomials",["3_3","3_4"]],
    ["8","Optimisation",["3_5"]],
    ["9-10","CurveSketching",["3_6"]],
    ["11","LHopital",["3_7"]],
    ["12","Antiderivatives",["4_1"]]
]

#################################################################
# End of compilation choices
#################################################################

#################################################################
# Make list of types to print (beamer, handout, prep)
#################################################################

type_list=[]
if print_beamer:
	type_list.append("beamer")
if print_handout:
	type_list.append("handout")
if print_prep:
	type_list.append("prep")



#################################################################
# Build function
## Given a filename in the scr directory: 
## build, put PDF in pdf file, clean up extraneous files
#################################################################

SOURCE_DIR = "src"
PDF_DIR = "pdfs"

def build_pdf(base_filename):
	if dry_run==True:
		print("Build ",base_filename)
		return
	#change directory
	os.chdir(SOURCE_DIR)
 	# run latex
	subprocess.run(["pdflatex", "-interaction=nonstopmode", base_filename])
	# # move the resulting pdf to the PDF directory
	shutil.move(
        base_filename + ".pdf", os.path.join("..", PDF_DIR, base_filename + ".pdf")
    )
 #    # go back into parent directory
	os.chdir("..")

#################################################################
# Build individual sections
## Given a section number, section title, and slide type, generate a .tex file
## build it using build_pdf
#################################################################

def onesection(sectionnumber,sectionname,slidetype):
	#create the new .tex file named with section number, name, and type
	#if it already exists, overwrite
	if slidetype=='beamer' or slidetype=='b':
		base_filename=sectionnumber+sectionname+'_Beamer'
		texFile=open(os.path.join('src',base_filename)+'.tex','w')
		texFile.write('\\documentclass[10pt]{beamer} ')
	elif slidetype=='handout' or slidetype=='h':
		base_filename=sectionnumber+sectionname+'_Handout'
		texFile=open(os.path.join('src',base_filename+'.tex'),'w')
		texFile.write('\\documentclass[10pt,handout]{beamer} ')
	elif slidetype=='prep' or slidetype=='p':
		base_filename=sectionnumber+sectionname+'_Prep'
		texFile=open(os.path.join('src',base_filename+'.tex'),'w')
		texFile.write('\\documentclass[10pt,handout]{beamer} \n')
		texFile.write('\\setbeameroption{show notes} ')
	else:
		print('second argument should be "beamer" or "b" for slides to show in class, "handout" or "h" for slides to give to students, or "prep" or "p" for slides with scripts and other instructor notes')

	#packages and begin{document} common to all types
	texFile.write('\n\n\\usepackage{header100} \n\\usepackage{header_maps} \n\n\\begin{document} \n\n')
	#input the section contents
	texFile.write('\\input{sections/'+sectionnumber+'.tex}\n')	
	#end tex file
	texFile.write('\\LastPage  \n\n\\end{document}')
	texFile.close()

	#build
	build_pdf(base_filename)


#################################################################
# Build file for entire week
#################################################################

def oneweek(weeknumber,weekname,sectionnumbers,slidetype):
	#create the file newfile.tex
	#if it already exists, overwrite
	if slidetype=='beamer' or slidetype=='b':
		if len(sectionnumbers)>1:
			base_filename="W"+weeknumber+weekname+"_"+sectionnumbers[0]+"-"+sectionnumbers[-1]+'_Beamer'
		else:
			base_filename="W"+weeknumber+weekname+"_"+sectionnumbers[0]+'_Beamer'
		texFile=open(os.path.join('src',base_filename)+'.tex','w')
		texFile.write('\\documentclass[10pt]{beamer} ')
	elif slidetype=='handout' or slidetype=='h':
		if len(sectionnumbers)>1:
			base_filename="W"+weeknumber+weekname+"_"+sectionnumbers[0]+"-"+sectionnumbers[-1]+'_Handout'
		else:
			base_filename="W"+weeknumber+weekname+"_"+sectionnumbers[0]+'_Handout'
		texFile=open(os.path.join('src',base_filename+'.tex'),'w')
		texFile.write('\\documentclass[10pt,handout]{beamer} ')
	elif slidetype=='prep' or slidetype=='p':
		if len(sectionnumbers)>1:
			base_filename="W"+weeknumber+weekname+"_"+sectionnumbers[0]+"-"+sectionnumbers[-1]+'_Prep'
		else:
			base_filename="W"+weeknumber+weekname+"_"+sectionnumbers[0]+'_Prep'
		texFile=open(os.path.join('src',base_filename+'.tex'),'w')
		texFile.write('\\documentclass[10pt,handout]{beamer} \n')
		texFile.write('\\setbeameroption{show notes} ')
	else:
		print('second argument should be "beamer" or "b" for slides to show in class, "handout" or "h" for slides to give to students, and "prep" or "p" for slides with scripts and other instructor notes')

	#packages and begin{document} common to all types
	texFile.write('\n\n\\usepackage{header100} \n\\usepackage{header_maps} \n\n\\begin{document} \n\n')
	
	#input all sections
	for y in sectionnumbers:
		texFile.write('\\input{sections/'+y+'.tex}\n')
	
	#end tex file
	texFile.write('\\LastPage  \n\n\\end{document}')
	texFile.close()

	#build
	build_pdf(base_filename)



#################################################################
# Make PDFs for all sections
#################################################################
if print_sections:
	for type in type_list:
		for section in section_names_list:
			onesection(section[0],section[1],type)

#################################################################
# Make PDFs for all weeks
#################################################################
if print_weeks:
	for type in type_list:
		for week_entry in week_list:
			oneweek(week_entry[0],week_entry[1],week_entry[2],type)

#################################################################
# Make PDFs for miscellaneous files
#################################################################
if print_studentworkbook:
	build_pdf('CLP1StudentWorkbook')

if print_review:
	for type in type_list:
		onesection('review','',type)

if print_readme:
	PDF_DIR = "." # ReadMe.pdf goes in the main directory
	build_pdf("ReadMe")
	PDF_DIR = "pdfs" #reset the pdf directory

