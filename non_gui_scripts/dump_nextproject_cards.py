#!/usr/bin/env python3
# Python script to dump card issue details from a given project column

import sys
from atdumpmemex import list_memex_cards

if len(sys.argv) != 3:
    print("   Usage: " + sys.argv[0] + " my-project-id my-column-id")
    sys.exit(1)

project_id = sys.argv[1]
column_id = sys.argv[2]

list_memex_cards(column_id, project_id)