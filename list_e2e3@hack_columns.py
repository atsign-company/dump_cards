#!/usr/bin/env python3
# Python script to list the columns in a given project ID

import sys
from atdumpcards import list_project_columns

project_id = "13148087"
org = "atsign-company"
        
list_project_columns(project_id, org)