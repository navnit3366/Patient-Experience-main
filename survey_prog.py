#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
"""

import random

#list of survey questions
px_q=['1-It was easy to make an appointment.',
            '2-Parking was adequate.',
            '3-Elevators and walk-ways had enough space for everyone.',
            '4-It was easy to find my way around.',
            '5-The facility was clean.',
            '6-I felt welcomed by the staff.',
            '7-I did not have to wait long to check in.',
            '8-Staff were expecting me; my appointment was in the system.',
            '9-I understood the reason for any fees and charges',
            '10-I felt relaxed in the waiting room.',
            '11-There was enough space for everyone in the waiting room.',
            '12-My appointment occurred at the expected time.',
            '13-My doctor was focused on me - not his/her computer.',
            '14-My doctor made me feel calm and supported',
            "15-My doctor took time to answer my questions.",
            "16-It was easy to get the prescriptions and services that my doctor ordered.",
            "17-I know exactly how to carry out all of my doctor's instructions."]

retention_q =["18-I would recommend this center to a friend or on social media.",
             "19-I want to re-enroll at my medical center."]

filein = open("respondents.txt", 'r')
rdata = filein.readlines()

#create list of responses
resplist=[]
for i in rdata:
    i=i.rstrip('\n')
    v=i.split(",")
    v[2]=int(v[2])
    v[6]=int(v[6])
    v[7]=float(v[7])
    resplist.append(v)

#put responses on likert scale            
def agree_answers(agreeresp):

    if agreeresp>.8:
        agreeansw="Strongly Agree"
        agreecode=5
    elif agreeresp<=.8 and agreeresp>.6:
        agreeansw="Agree"
        agreecode=4
    elif agreeresp<=.6 and agreeresp>.5:
        agreeansw="Neither Agree nor Disagree"
        agreecode=3
    elif agreeresp<=.5 and agreeresp>.3:
        agreeansw="Disagree"
        agreecode=2
    else:
        agreeansw="Strongly Disagree"
        agreecode=1
    respondent.append(agreecode)

def retention(rr_response):

    if rr_response>.8:
        rr_answer="Strongly Agree"
        rr_code=5
    elif rr_response<=.8 and rr_response>.6:
        rr_answer="Agree"
        rr_code=4
    elif rr_response<=.6 and rr_response>.4:
        rr_answer="Neutral"
        rr_code=3
    elif rr_response<=.4 and rr_response>.2:
        rr_answer="Disagree"
        rr_code=2
    else:
        rr_answer="Strongly Disagree"
        rr_code=1
    respondent.append(rr_code)

def survey_px(respondent):
    shift=respondent[7]
    agreesum=0
    for q in px_q:
        if q==px_q[7]:
            agreeresp=random.uniform(shift,shift+.7)#trouble spot 
        elif q==px_q[15]:
            agreeresp=random.uniform(shift,shift+.5)#trouble spot that improves in Q3-Q4
        elif q==px_q[2]:
            agreeresp=random.uniform(0,shift-.1)
        else:
            agreeresp=random.uniform(shift,shift+1)
        agree_answers(agreeresp)
        agreesum=agreesum+agreeresp  
        agreemean=agreesum/len(px_q)
        
    for q in retention_q:
        rr_response=agreemean+random.gauss(0,.5)
        retention(rr_response)
        print(agreemean,rr_response)

#Ask the survey questions 
for respondent in resplist:
    survey_px(respondent)

#Write the responses to a file
def write_data(resplist):
    for i in resplist:
        fileout=open("survey_data_codes10.txt",'a')
        patid=i[0]
        loc=i[1]
        age=str(i[2])
        sex=i[3]
        doc=i[4]
        lang=i[5]
        surv=str(i[6])
        shift=str(i[7])

        appointment=str(i[8])
        fac_parking=str(i[9])
        fac_elev=str(i[10])
        fac_navigate=str(i[11])
        fac_clean=str(i[12])

        reception_welcome=str(i[13])
        reception_checkin=str(i[14])
        reception_expected=str(i[15])
        reception_fees=str(i[16])
        reception_atmosphere=str(i[17])
        reception_waitingroom=str(i[18])
        reception_ontime=str(i[19])

        doc_focused=str(i[20])
        doc_supported=str(i[21])
        doc_answered=str(i[22])
        doc_followup=str(i[23])
        doc_carryout=str(i[24])

        recommend=str(i[25])
        reenroll=str(i[26])

        fileout.write(patid)
        fileout.write(",")
        fileout.write(loc)
        fileout.write(",")
        fileout.write(age)
        fileout.write(",")
        fileout.write(sex)
        fileout.write(",")
        fileout.write(doc)
        fileout.write(",")
        fileout.write(lang)
        fileout.write(",")
        fileout.write(surv)
        fileout.write(",")
        fileout.write(shift)
        fileout.write(",")
        fileout.write(appointment)
        fileout.write(",")
        fileout.write(fac_parking)
        fileout.write(",")
        fileout.write(fac_elev)
        fileout.write(",")
        fileout.write(fac_navigate)
        fileout.write(",")
        fileout.write(fac_clean)
        fileout.write(",")
        fileout.write(reception_welcome)
        fileout.write(",")
        fileout.write(reception_checkin)
        fileout.write(",")
        fileout.write(reception_expected)
        fileout.write(",")
        fileout.write(reception_fees)
        fileout.write(",")
        fileout.write(reception_atmosphere)
        fileout.write(",")
        fileout.write(reception_waitingroom)
        fileout.write(",")
        fileout.write(reception_ontime)
        fileout.write(",")
        fileout.write(doc_focused)
        fileout.write(",")
        fileout.write(doc_supported)
        fileout.write(",")
        fileout.write(doc_answered)
        fileout.write(",")
        fileout.write(doc_followup)
        fileout.write(",")
        fileout.write(doc_carryout)
        fileout.write(",")
        fileout.write(recommend)
        fileout.write(",")
        fileout.write(reenroll+"\n")
        fileout.close

write_data(resplist)


