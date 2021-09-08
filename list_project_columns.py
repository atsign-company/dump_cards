#!/usr/bin/env python3
# Python script to list the columns in a given project ID

import sys
from atdumpcards import list_project_columns

if len(sys.argv) != 3:
    print("   Usage: " + sys.argv[0] + " my-project-id org_name")
    sys.exit(1)

project_id = sys.argv[1]
org = sys.argv[2]
        
list_project_columns(project_id, org)