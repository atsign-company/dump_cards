#!/usr/bin/env python3
# Python script to dump card issue details from a given project column

import sys
from atdumpcards import list_project_cards

if len(sys.argv) != 2:
    print("   Usage: " + sys.argv[0] + " my-column-id")
    sys.exit(1)

column_id = sys.argv[1]

list_project_cards(column_id)