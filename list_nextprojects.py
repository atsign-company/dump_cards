#!/usr/bin/env python3
# Python script to list the projects in an organization

import base64, json, sys
from atdumpmemex import list_memex_projects

if len(sys.argv) != 2:
    print("   Usage: " + sys.argv[0] + " org_name")
    sys.exit(1)

org = sys.argv[1]
        
json_projects = list_memex_projects(org)
for node in json_projects["data"]["organization"]["projectsNext"]["nodes"]:
        project_id = base64.b64decode(node["id"]).decode("utf-8")
        print(f'{project_id}  {node["title"]}')