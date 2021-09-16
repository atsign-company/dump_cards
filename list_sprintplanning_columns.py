#!/usr/bin/env python3
# Python script to list the columns in a given project ID

from atdumpcards import list_project_columns

project_id = "6018453"
org = "atsign-foundation"
        
json_columns = list_project_columns(project_id, org)
for column in json_columns:
        print(f'{column["id"]} {column["name"]}')