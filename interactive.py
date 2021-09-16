#!/usr/bin/env python3
# pip3 install InquirerPy
import sys
from InquirerPy import inquirer
from atdumpmemex import *
from atdumpcards import * 

# create empty lists for later appends
pchoice = []
cchoice = []
orglist = []

for orgs in list_orgs():
    orglist.append(orgs["organization"]["login"])
if not orglist:
    print("User isn't a member of any orgs")
    sys.exit()

org = inquirer.select(message="Which org?",
    choices=orglist).execute()
ptype = inquirer.select(message="Normal or beta?",
    choices=["normal","beta"]).execute()

if ptype == "beta":
    json_projects = list_memex_projects(org)
    for node in json_projects["data"]["organization"]["projectsNext"]["nodes"]:
        project_id = base64.b64decode(node["id"]).decode("utf-8")
        pchoice.append(project_id+' '+node["title"])
    if not pchoice:
        print("No projects found")
        sys.exit()
    project_id = inquirer.select(message="Which project?",
       choices=pchoice).execute()
    json_columns = list_memex_columns(project_id.partition(" ")[0])
    if not json_columns:
        print("No columns found")
        sys.exit()
    column_id = inquirer.select(message="Which column?",
       choices=json_columns).execute()
    list_memex_cards(column_id.partition(" ")[0],project_id.partition(" ")[0])
    print("Exported: "+column_id.partition(" ")[0]+".csv")
else:
    json_projects = list_projects(org)
    for project in json_projects:
        pchoice.append(str(project["id"])+' '+str(project["number"])+' '
            +project["name"])
    if not pchoice:
        print("No projects found")
        sys.exit()
    project_id = inquirer.select(message="Which project?",
       choices=pchoice).execute()
    json_columns = list_project_columns(project_id.partition(" ")[0])
    for column in json_columns:
        cchoice.append(str(column["id"])+' '+column["name"])
    if not cchoice:
        print("No columns found")
        sys.exit()
    column_id = inquirer.select(message="Which column?",
       choices=cchoice).execute()
    list_project_cards(column_id.partition(" ")[0], org)
    print("Exported: "+column_id.partition(" ")[0]+".csv")