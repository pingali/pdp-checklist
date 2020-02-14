#!/usr/bin/python3

import os
import json
import csv
from collections import OrderedDict

codes = {
    "L": "Legal/Compliance",
    "P": "Public Relations",
    "T": "Technical and IT",
    "H": "HR",
    "C": "Customer Relations",

    "DF": "Data Fiduciaries",
    "DP": "Data Processors",
    
}

overview = list(csv.DictReader(open("overview.csv")))
introduction = overview[0]['SubjectDescription']

checklist = OrderedDict([])
for entry in overview[1:]:

    #['Provisions', 'Groups', 'Subsection', 'PartTitle', 'Functions',
    #'Subject', 'Section', 'SubjectDescription', 'Part',
    #'SectionTitle', 'SubsectionTitle', 'SubjectTitle']

    section = entry['Section']
    sectiontitle = entry['SectionTitle']

    if section not in checklist:
        checklist[section] = {
            'section': section,
            'title': sectiontitle,
            'subjects': OrderedDict([])
        }

    subject = entry['Subject'].strip()
    subjecttitle = entry['SubjectTitle']    
    subsectiontitle = entry['SubsectionTitle']    

    groups = entry['Groups']
    functions = entry['Functions']
    description = entry['SubjectDescription']
    provisions = entry['Provisions']

    # lookup the codes
    groups = [codes[x.strip()] for x in groups.split(",")]
    functions = [codes[x.strip()] for x in functions.split(",")]
    
    if subject not in checklist[section]['subjects']:
        checklist[section]['subjects'][subject] = {
            'subject': subject,
            'title': subjecttitle,
            'groups': groups,
            'description': description,
            'functions': functions,
            'provisions': provisions, 
            'actions': OrderedDict()
        }


    #actions = checklist[section]['subjects']['actions']

actions = list(csv.DictReader(open("actions.csv")))
for entry in actions:

    section = entry['Section'].strip()
    subject = entry['Subject'].strip()
    actionnum = entry['ActionNumber'].strip()
    action    = entry['Action'].strip()

    checklist[section]['subjects'][subject]['actions'][actionnum] = {
        'no': actionnum,
        'description': action
    }
    
overview = {
    'overview': introduction,
    'checklist': checklist
}
print(json.dumps(overview, indent=4))
