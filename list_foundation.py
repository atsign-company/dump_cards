#!/usr/bin/env python3
# Python script to list the projects in an organization

import sys
from atdumpcards import list_projects

org = "atsign-foundation"
        
list_projects(org)