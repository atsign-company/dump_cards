#!/usr/bin/env python3
# Python script to list the columns in a given project ID

from atdumpmemex import list_memex_columns

project_id = "011:ProjectNext3594"

print(f'Project ID: {project_id}')
json_columns = list_memex_columns(project_id)
for column in json_columns:
    print(column)