#!/usr/bin/env python3
# Python script to list the columns in a given project ID

import sys
from atdumpcards import list_project_columns

if len(sys.argv) != 3:
    print("   Usage: " + sys.argv[0] + " my-project-id org_name")
    sys.exit(1)

project_id = sys.argv[1]
org = sys.argv[2]
        
json_columns = list_project_columns(project_id, org)
for column in json_columns:
        print(f'{column["id"]} {column["name"]}')