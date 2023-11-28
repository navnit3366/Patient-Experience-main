# !/usr/bin/env python 3

print("Content-type: text/html\n\n")
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#read data created in survey_prog
df = pd.read_csv('survey_data_codes10.txt',names=

        ['patid',
         'Medical_Home',
         'age',
         'Sex',
         'doctorid',
         'Language',
         'survey_quarter',
         'shift',
         'appointment',
         'fac_parking',
         'fac_uncrowded',
         'fac_navigate',
         'fac_clean',
         'r_welcome',
         'r_checkin',
         'r_expected',
         'r_fees',
         'r_atmosphere',
         'r_waitingroom',
         'r_ontime',
         'doctor_focused',
         'doctor_supportive',
         'doc_answered_questions',
         'followup_service_quality',
         'followup_carryout',
         'recommend',
         'reenroll'])

#Make lists of variable names and question titles
vanames=list(df.columns[8:27])
questiontitles=[
            'It was easy to make an appointment.',
            'Parking was adequate.',
            'Elevators and walk-ways had enough space for everyone.',
            'It was easy to find my way around.',
            'The facility was clean.',
            'I felt welcomed by the staff.',
            'I did not have to wait long to check in.',
            'Staff were expecting me; my appointment was in the system.',
            'I understood the reason for any fees and charges',
            'I felt relaxed in the waiting room.',
            'There was enough space for everyone in the waiting room.',
            'My appointment occurred at the expected time.',
            'My doctor was focused on me - not his/her computer.',
            'My doctor made me feel calm and supported',
            "My doctor took time to answer my questions.",
            "It was easy to get the prescriptions and services that my doctor ordered.",
            "I know exactly how to carry out my doctor's instructions.",
            "I'd recommend this center to friends/on social media.",
            "I want to re-enroll at my medical center."]


# Recode the Age variable for analysis

def recode(df):
    df["intage"]=df['age'].astype(int)
    bins = [0,65,100]
    names = ['Less than 65', '65+']
    df['AgeRange'] = pd.cut(df['intage'], bins, labels=names)
    return df['AgeRange']
recode(df)

#Check data with xtabs
try:
    pd.crosstab(df['survey_quarter'], df['reenroll'],normalize=True,margins=True)
except:
    print("No crosstab produced.")


#Create elements for HTML table: Percent Agree

sumlist=[]
nlist=[]
perclist=[]
def percentagree(df):
    for i in df.columns[8:27]:
        xagree=(df[i]==5) | (df[i]==4)
        xasum=xagree.sum()
        xacount=xagree.count()
        xaperc=round(100*xasum/xacount,1)
        sumlist.append(xasum)
        nlist.append(xacount)
        perclist.append(xaperc)
    return nlist , perclist
percentagree(df)

#Create elements for HTML table:  counts

sagreelist=[]
agreelist=[]
neutlist=[]
disagreelist=[]
sdisagreelist=[]
def counts(df,nlist,perclist):
    for i in df.columns[8:27]:
        sagree=df[i]==5
        agree=df[i]==4
        neut=df[i]==3
        disagree=df[i]==2
        sdisagree=df[i]==1

        sagree_sum=sagree.sum()
        agree_sum=agree.sum()
        neut_sum=neut.sum()
        disagree_sum=disagree.sum()
        sdisagree_sum=sdisagree.sum()

        sagreelist.append(sagree_sum)
        agreelist.append(agree_sum)
        neutlist.append(neut_sum)
        disagreelist.append(disagree_sum)
        sdisagreelist.append(sdisagree_sum)
    listoflist=[questiontitles,nlist,sdisagreelist,disagreelist,neutlist,agreelist,sagreelist,perclist]
    tabcells=pd.DataFrame(listoflist)
    tabcells_trans=tabcells.transpose()
    tabcells_trans.columns=['Question', 'Count', 'SDisagree', 'Disagree','Neut','Agree','Sagree','perc']
    tabcells_trans.to_csv('tabelems.csv', index=False)


counts(df,nlist,perclist)

# Create HTML table

filein = open('tabelems.csv',"r")
fileout = open("html-table_surv.html", "w")
tabledata = filein.readlines()

table = "<!DOCTYPE HTML>\n <http>\n"
table = table + "<head>\n <h1>Summary of Responses: Extent of patients' agreement with PX statements</h1>\n"
table = table + "<style>\n"
table = table + "table.center\n"
table = table + "table, td, th {width:100%; font-family:verdana;font-size:9;border: 1px black; border-collapse: collapse;padding: 8px;}\n"
table = table + "td {text-align: center;}\n"
table = table + "td:first-child {text-align: left;}\n"
table = table + "th {width:80px;background-color:#008B8B;color: white;word-wrap: normal;}\n"
table = table + "tr:nth-child(even) {background-color:  #FFFFF0;}\n"
table = table + "</style>\n </head>\n  <body>\n"
table = table + "<table class='center'>\n"

header=['Question',"Response Count","Strongly Disagree Count","Disagree Count","Neutral Count","Agree Count","Strongly Agree Count","Percent Favorable"]
table = table + "  <tr>\n"  #adds the first row which is the header
for column in header:
    table += "<th>{0}</th>".format(column)
table += "  </tr>\n"

for line in tabledata[1::]:
    elem = line.split(",")
    table =table+ "  <tr>"
    for column in elem:
        table = table + "<td>{0}</td>".format(column)
    table += "  </tr>\n"

table += "</table>"
table +="</body>"
table += "</html>"

fileout.writelines(table)
fileout.close()

#Create charts for pxcenter.html home page

demovars=['Medical_Home','Sex','Language','AgeRange']

def frontcharts(df):
    for i in demovars:
        df.pivot_table(df.columns[25], [i], 'survey_quarter',aggfunc='mean',dropna=True).plot.bar()
        plt.xticks(rotation=0,fontsize=14)
        plt.ylabel('Avg. Agreement \n (1=Lowest, 5=Highest',fontsize=14)
        plt.ylim(0,5)
        plt.legend(ncol=4,loc=9,title="Survey Quarter",fontsize=12)
        plt.title("By {x}: {0}".format(questiontitles[17],x=i),fontsize=16,wrap=True)
        plt.savefig("html_charts/"+i+'fig_home.png')
        plt.close()

frontcharts(df)

#Create detailed charts for each patient pop group and save for child pages

def charts_by_sex(df):
    qindex=0
    nobs=str(len(df))
    for i in df.columns[8:27]:
        df.pivot_table(i, 'Sex', 'survey_quarter',dropna=True,aggfunc='mean').plot.bar()
        plt.xticks(rotation=0,fontsize=14)
        plt.ylabel('Avg. Agreement \n (1=Lowest, 5=Highest',fontsize=14)
        plt.ylim(0,5)
        plt.legend(ncol=4,loc=9,title="Survey Quarter",fontsize=12)
        plt.title(questiontitles[qindex] + " (N=" + nobs+")",fontsize=16,wrap=True)
        plt.savefig("html_charts/fig_sex_breakout"+i)
        plt.close()
        qindex=qindex+1

charts_by_sex(df)

def charts_by_language(df):
    qindex=0
    nobs=str(len(df))
    for i in df.columns[8:27]:
        df.pivot_table(i, 'Language', 'survey_quarter',dropna=True,aggfunc='mean').plot.bar()
        plt.xticks(rotation=0,fontsize=14)
        plt.ylabel('Avg. Agreement \n (1=Lowest, 5=Highest',fontsize=14)
        plt.ylim(0,5)
        plt.legend(ncol=4,loc=9,title="Survey Quarter",fontsize=12)
        plt.title(questiontitles[qindex] + " (N=" + nobs+")",fontsize=16,wrap=True)
        plt.savefig("html_charts/fig_lang_breakout"+i)
        plt.close()
        qindex=qindex+1

charts_by_language(df)

def charts_by_age(df):
    qindex=0
    nobs=str(len(df))
    for i in df.columns[8:27]:
        df.pivot_table(i, 'AgeRange', 'survey_quarter',dropna=True,aggfunc='mean').plot.bar()
        plt.xticks(rotation=0,fontsize=14)
        plt.ylabel('Avg. Agreement \n (1=Lowest, 5=Highest',fontsize=14)
        plt.ylim(0,5)
        plt.legend(ncol=4,loc=9,title="Survey Quarter",fontsize=12)
        plt.title(questiontitles[qindex] + " (N=" + nobs+")",fontsize=16,wrap=True)
        plt.savefig("html_charts/fig_age_breakout"+i)
        plt.close()
        qindex=qindex+1

charts_by_age(df)

def charts_by_medhome(df):
    qindex=0
    nobs=str(len(df))
    for i in df.columns[8:26]:
        df.pivot_table(i, 'Medical_Home', 'survey_quarter',dropna=True,aggfunc='mean').plot.bar()
        plt.xticks(rotation=0,fontsize=14)
        plt.ylabel('Avg. Agreement \n (1=Lowest, 5=Highest',fontsize=14)
        plt.ylim(0,5)
        plt.legend(ncol=4,loc=9,title="Survey Quarter",fontsize=12)
        plt.title(questiontitles[qindex] + " (N=" + nobs+")",fontsize=16,wrap=True)
        plt.savefig("html_charts/fig_medhome_breakout"+i)
        plt.close()
        qindex=qindex+1

charts_by_medhome(df)

#Create charts relating recommendation and reenrollment responses to other survey answers
#Save for child pages
def recommendation_charts(df):
    metric=df.columns[25]
    metric_quest=questiontitles[17]
    qindex=0
    nobs=str(len(df))
    for i in df.columns[8:25]:
        boxprops = dict(linestyle='-', linewidth=3, color='g')
        medianprops= dict(linestyle='--', linewidth=2.5, color='m')
        meanpointprops = dict(marker='D', markeredgecolor='black',markerfacecolor='red')
        boxplot = df.boxplot(column=[df.columns[25]],by=[i],showmeans=True,meanprops=meanpointprops,boxprops=boxprops,medianprops=medianprops,grid=False)
        plt.title(metric_quest + " (N=" + nobs+")",fontsize=16,wrap=True)
        plt.xlabel(questiontitles[qindex] + "(1=Lowest, 5=Highest)",wrap=True,fontsize=12)
        plt.suptitle("")
        plt.subplots_adjust(bottom=0.2)
        plt.ylabel('Agreement \n (1=Lowest, 5=Highest',fontsize=12)
        plt.xticks(rotation=0)
        plt.savefig("html_charts/fig_rec"+i)
        plt.close()
        qindex=qindex+1

recommendation_charts(df)

def reenrollment_charts(df):
    try:
        metric=df.columns[26]
        metric_quest=questiontitles[18]
        qindex=0
        nobs=str(len(df))
        for i in df.columns[8:25]:
            boxprops = dict(linestyle='-', linewidth=3, color='g')
            medianprops= dict(linestyle='--', linewidth=2.5, color='m')
            meanpointprops = dict(marker='D', markeredgecolor='black',markerfacecolor='red')
            boxplot = df.boxplot(column=[df.columns[26]],by=[i],showmeans=True,meanprops=meanpointprops,boxprops=boxprops,medianprops=medianprops,grid=False)
            plt.title(metric_quest + " (N=" + nobs+")",fontsize=16,wrap=True)
            plt.xlabel(questiontitles[qindex] + "(1=Lowest, 5=Highest)",wrap=True,fontsize=12)
            plt.suptitle("")
            plt.subplots_adjust(bottom=0.2,left=.2)
            plt.ylabel('Agreement \n (1=Lowest, 5=Highest',fontsize=12)
            plt.xticks(rotation=0)
            plt.savefig("html_charts/fig_reenroll"+i)
            plt.close()
            qindex=qindex+1
    except:
        print("No chart produced.")

reenrollment_charts(df)

#Create correlations and correlation tables for recommendation and reenrollment child pages
def reenroll_corrs(df):
    try:
        metric_quest=questiontitles[18]
        varnames=list(df.columns[8:25])
        coefflist_reen=[]
        for i in df.columns[8:25]:
            cf=df['reenroll'].corr(df[i])
            coefflist_reen.append(cf)
        plt.barh(varnames,coefflist_reen)
        plt.xlabel("Correlation Coefficient")
        plt.title("Correlations to: "+metric_quest,wrap=True)
        plt.savefig("Renroll_corrs.png",bbox_inches='tight')
        plt.show()
        plt.close()
    except:
        print("No chart produced.")

reenroll_corrs(df)

def rec_corrs(df):
    try:
        metric_quest=questiontitles[17]
        varnames=list(df.columns[8:25])
        coefflist_rec=[]
        for i in df.columns[8:25]:
            cf=df['recommend'].corr(df[i])
            coefflist_rec.append(cf)
        plt.barh(varnames,coefflist_rec)
        plt.xlabel("Correlation Coefficient")
        plt.title("Correlations to: "+metric_quest,wrap=True)
        plt.savefig("recommend_corrs.png",bbox_inches='tight')
        plt.show()
        plt.close()
    except:
        print("No chart produced.")

rec_corrs(df)

filein.close()
















































































































































