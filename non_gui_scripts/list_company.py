#!/usr/bin/env python3
# Python script to list the projects in an organization

from atdumpcards import list_projects

org = "atsign-company"
        
json_projects = list_projects(org)
for project in json_projects:
    print(f'{project["id"]} {project["number"]} {project["name"]}')