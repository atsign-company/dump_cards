#!/usr/bin/env python3
# Python script to list the projects in an organization

import sys
from atdumpmemex import list_memex_projects

if len(sys.argv) != 2:
    print("   Usage: " + sys.argv[0] + " org_name")
    sys.exit(1)

org = sys.argv[1]
        
list_memex_projects(org)