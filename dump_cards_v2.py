#!/usr/bin/env python3
# pip3 install InquirerPy
import base64, sys
from InquirerPy import inquirer
from atdumpcardsv2 import *
from atdumpcards import * 

# Create empty lists for later appends
orglist = []
pchoice = []
cchoice = []

# Get org list from API
for orgs in list_orgs():
    orglist.append(orgs["organization"]["login"])
if not orglist:
    print("User isn't a member of any orgs")
    sys.exit()

# User selects org from list
org = inquirer.select(message="Which org?",
    choices=orglist).execute()

# Get regular projects from API
json_projects = list_projects(org)
for project in json_projects:
    pchoice.append(str(project["number"])+' '+str(project["id"])
        +' '+project["name"])
#Get V2 projects from API
json_bprojects = list_v2_projects(org)
for node in json_bprojects["data"]["organization"]["projectsV2"]["nodes"]:
    #proj_num = str(node["number"])
    proj_id = node["id"]
    if not node["closed"]:
        pchoice.append('v2 '+proj_id+' '+node["title"])
if not pchoice:
    print("No projects found")
    sys.exit()
# User selects project from list
pselect = inquirer.select(message="Which project?",
    choices=pchoice).execute()
project_id = pselect.partition(" ")[2].partition(" ")[0]
# V2 projects
if pselect.partition(" ")[0] == 'v2':
    json_fields = list_v2_fields(project_id)
    if not json_fields:
        print("No fields found")
        sys.exit()
    json_columns = list_v2_fields(project_id)
    field = inquirer.select(message="Which field?",
      choices=json_fields).execute()
    field_id = field.partition(" ")[0]
    field_name = field.partition(" ")[1]
    json_columns = list_v2_columns(field_id)
    if not json_columns:
      print("No columns found")
      sys.exit()
    column_name = inquirer.select(message="Which column?",
       choices=json_columns).execute()
    list_v2_cards(field_id,project_id,column_name)
    print("Exported: "+column_name+".csv")
else:
# Regular projects
    json_columns = list_project_columns(project_id)
    for column in json_columns:
        cchoice.append(str(column["id"])+' '+column["name"])
    if not cchoice:
        print("No columns found")
        sys.exit()
    column_id = inquirer.select(message="Which column?",
       choices=cchoice).execute().partition(" ")[0]
    list_project_cards(column_id)
    print("Exported: "+column_id+".csv")