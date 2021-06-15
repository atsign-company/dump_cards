#!/usr/bin/env python3
# Python script to list the projects in an organization

import os, sys, json, requests, yaml

# Color constants
# Reference: https://gist.github.com/chrisopedia/8754917
COLERR="\033[0;31m"
COLINFO="\033[0;35m"
COLRESET="\033[m"

baseurl = 'https://api.github.com'
headers = {"Content-Type": "application/json", "Accept": "application/vnd.github.inertia-preview+json"}

if len(sys.argv) != 2:
    print("   Usage: " + sys.argv[0] + " org_name")
    sys.exit(1)

org = sys.argv[1]
token = os.environ['GITHUB_API_TOKEN']

def list_projects():
    # Get list of all repos in an org
    response = requests.get(baseurl + "/orgs/" + org + "/projects", 
        headers=headers, 
        auth=(org, token))
    if response.status_code != 200:
        # An error occured
        print(COLERR + "Error getting project columns : " + str(response.status_code) + " " + response.text
        + COLRESET)

    # Convert repos to YAML
    json_projects = json.loads(response.text)
    #print(json.dumps(json_projects, indent=4, sort_keys=True))
    for project in json_projects:
        print(f'{project["id"]} {project["number"]} {project["name"]}')
        
list_projects()