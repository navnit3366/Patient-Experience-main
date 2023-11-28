#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

"""

import random
from numpy.random import choice

#Patient's adminstrative data
def locanswers(loc):
    if loc==1:
        loccode='home1'
    else:
        loccode='home2'
    patient.append(loccode)

def ageanswers(age):
    agestr=str(age)
    patient.append(agestr)

def gendercode(sex):
    if sex==0:
        gender="Female"
    elif sex==1:
        gender="Male"
    patient.append(gender)

def primarycare_doc(docid):
    pc_doctor="PC"+str(docid)
    patient.append(pc_doctor)

def language(lang):
    patient.append(lang)

#Numpats is number of patients;  initiate patient list
patientlist=[]
def setpatlist(numpats):
    for i in range(numpats):
        list=[]
        num=100+i
        patid="PAT"+str(num)
        list.append(patid)
        patientlist.append(list)

numpats=500
setpatlist(numpats)
#Numpats is number of patients;  initiate patient list

#Generate admin data
def pat_admin(patient):

    loc = random.randint(0,1)
    locanswers(loc)

    age=int(round(random.triangular(18,90,45),0))
    ageanswers(age)

    sex=random.randint(0,1)
    gendercode(sex)

    docid=random.randint(1,50)
    primarycare_doc(docid)

    #data:https://datausa.io/profile/geo/fairfax-county-va
    langlist=["English","Spanish","Other"]
    langweights=[.65,.10,.25]
    lang=choice(langlist, p=langweights)
    language(lang)


for patient in patientlist:
    pat_admin(patient)

def write_data(patientlist):
    for i in patientlist:
        fileout=open("/home/cmoore48/public_html/patients.txt",'a')
        patid=i[0]
        medhome=i[1]
        age=i[2]
        gen=i[3]
        pcprovider=i[4]
        lang=i[5]
        fileout.write(patid)
        fileout.write(",")
        fileout.write(medhome)
        fileout.write(",")
        fileout.write(age)
        fileout.write(",")
        fileout.write(gen)
        fileout.write(",")
        fileout.write(pcprovider)
        fileout.write(",")
        fileout.write(lang + "\n")
        fileout.close
write_data(patientlist)
                                                                                                                                                            100,1         Bot
