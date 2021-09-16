#!/usr/bin/env python3
# Python script to list the columns in a given project ID

import sys
from atdumpmemex import list_memex_columns

if len(sys.argv) != 2:
    print("   Usage: " + sys.argv[0] + " my-project-id")
    sys.exit(1)

project_id = sys.argv[1]
        
json_columns = list_memex_columns(project_id)
for column in json_columns:
    print(column)