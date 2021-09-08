#!/usr/bin/env python3
# Python script to dump card issue details from a given project column

import sys
from atdumpcards import list_project_cards

if len(sys.argv) != 3:
    print("   Usage: " + sys.argv[0] + " my-column-id org_name")
    sys.exit(1)

column_id = sys.argv[1]
org = sys.argv[2]

list_project_cards(column_id, org)