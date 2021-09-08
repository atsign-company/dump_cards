#!/usr/bin/env python3
# Python script to list the columns in a given project ID

import sys
from atdumpcards import list_project_columns

project_id = "12437918"
org = "atsign-foundation"
        
list_project_columns(project_id, org)