#!/usr/bin/env python3
# Python script to list the columns in a given project ID

from atdumpcards import list_project_columns

project_id = "6018453"
        
json_columns = list_project_columns(project_id)
for column in json_columns:
        print(f'{column["id"]} {column["name"]}')