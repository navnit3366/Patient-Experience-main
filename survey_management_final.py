#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

"""
import random

filein = open("patients.txt", 'r')
pdata = filein.readlines()

#Add survey response characteristics to patient list
respondents=[]
for i in pdata:
    i=i.rstrip('\n')
    v=i.split(",")
    surv_period=random.randint(1,4)#quarter patient took survey
    v.append(surv_period)
    respondents.append(v)

for i in respondents:
    shift=0
    if i[6]==1:
        shift=-.1 #improvement over time
    elif i[6]==2:
        shift = 0
    elif i[6]==3:
        shift = .1
    elif i[6]==4:
        shift=.2
    if i[1]=='home1':
        shift=shift+.05
    if i[1]=='home2' and i[5]=="Other":
        shift=shift-.1
    if i[5]=="English":
        shift=shift+.1
    if int(i[2])>=65:
        shift=shift+.1
    if i[3]=="Female":
        shift=shift+.08
    shift=round(shift,3)
    i.append(shift)

def write_data(respondents):
    for i in respondents:
        fileout=open("respondents.txt",'a')
        patid=i[0]
        medhome=i[1]
        age=i[2]
        gen=i[3]
        pcprovider=i[4]
        lang=i[5]
        surv=str(i[6])
       shift=str(i[7])
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
        fileout.write(lang)
        fileout.write(",")
        fileout.write(surv)
        fileout.write(",")
        fileout.write(shift+ "\n")
        fileout.close
write_data(respondents)

