#!/usr/bin/env python3 

import json
import os
import json
import csv
from collections import OrderedDict

import click 
from mdutils import MdUtils

codes = {
    "L": "Legal/Compliance",
    "P": "Public Relations",
    "T": "Technical and IT",
    "H": "HR",
    "C": "Customer Relations",

    "DF": "Data Fiduciaries",
    "DP": "Data Processors",
    
}
flatten = lambda l: [item for sublist in l for item in sublist]

@click.group()
def process():
    """
    Preprocess and generate markdown
    """
    pass

@process.command('extract')
def extract():
    """
    Preprocess csvs 
    """
    overview = list(csv.DictReader(open("overview.csv")))
    introduction = overview[0]['SubjectDescription']

    checklist = OrderedDict([])
    for entry in overview[1:]:
        
        section = entry['Section']
        sectiontitle = entry['SectionTitle']
        if section not in checklist:
            checklist[section] = {
                'no': section,
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
                'no': subject,
                'title': subjecttitle,
                'groups': groups,
                'description': description,
                'functions': functions,
                'provisions': provisions, 
                'actions': OrderedDict()
            }


    actions = list(csv.DictReader(open("actions.csv")))
    for entry in actions:

        section = entry['Section'].strip()
        subject = entry['Subject'].strip()
        actionnum = entry['ActionNumber'].strip()
        action    = entry['Action'].strip()

        actions = checklist[section]['subjects'][subject]['actions']
        actions[actionnum] = {
            'no': actionnum,
            'title': "Action {}".format(actionnum),
            'description': action,
        }
        
    overview = {
        'title': 'Ikigai PDP 2019 Checklist',
        'overview': introduction,
        'checklist': checklist
    }
    
    print(json.dumps(overview, indent=4))

@process.command('markdown')
@click.argument('checklist')
def _markdown(checklist):
    """
    Generate markdown for checklist
    """

    checklist = json.load(open(checklist),  object_pairs_hook=OrderedDict)

    mdFile = MdUtils(file_name='Ikigai-Checklist',
                     title='PDP 2019 Checklist')


    mdFile.new_paragraph(checklist['overview'])

    sections = sorted(checklist['checklist'].values(),
                      key=lambda s: int(s['no']))
    for section in sections:
        mdFile.new_header(level=1, title=section['title'])
        for subject in section['subjects'].values():
            mdFile.new_header(level=2, title=subject['title'])
            mdFile.new_paragraph(subject['description'])
            mdFile.new_paragraph("Reference: " + subject['provisions'])
            mdFile.new_paragraph("Functions: " + ", ".join(subject['functions']))
            mdFile.new_paragraph("Groups: " + ", ".join(subject['groups']))

            actions = [['No','Description', 'Check']]
            actions += [[a['no'], a['title'], a['description']] for a in subject['actions'].values()]
            rows = len(actions) 
            actions = flatten(actions)
            mdFile.new_table(columns=3, rows=rows,
                             text=actions,
                             text_align='left')

    mdFile.create_md_file()
if __name__ == '__main__':
    process()
