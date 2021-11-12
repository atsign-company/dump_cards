#!/usr/bin/env python3
# pip3 install InquirerPy
import base64, sys
from InquirerPy import inquirer
from atdumpmemex import *
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
#Get beta projects from API
json_bprojects = list_memex_projects(org)
for node in json_bprojects["data"]["organization"]["projectsNext"]["nodes"]:
    #proj_num = str(node["number"])
    proj_id = node["id"]
    if not node["closed"]:
        pchoice.append('b '+proj_id+' '+node["title"])
if not pchoice:
    print("No projects found")
    sys.exit()
# User selects project from list
pselect = inquirer.select(message="Which project?",
    choices=pchoice).execute()
project_id = pselect.partition(" ")[2].partition(" ")[0]
# Beta projects
if pselect.partition(" ")[0] == 'b':
    json_columns = list_memex_columns(project_id)
    if not json_columns:
        print("No columns found")
        sys.exit()
    column_id = inquirer.select(message="Which column?",
       choices=json_columns).execute().partition(" ")[0]
    list_memex_cards(column_id,project_id)
    print("Exported: "+column_id+".csv")
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