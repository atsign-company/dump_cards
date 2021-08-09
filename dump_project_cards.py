#!/usr/bin/env python3
# Python script to dump card issue details from a given project column

import os, sys, json, requests, yaml

# Color constants
# Reference: https://gist.github.com/chrisopedia/8754917
COLERR="\033[0;31m"
COLINFO="\033[0;35m"
COLRESET="\033[m"

baseurl = 'https://api.github.com'
headers = {"Content-Type": "application/json", "Accept": "application/vnd.github.inertia-preview+json"}

if len(sys.argv) != 3:
    print("   Usage: " + sys.argv[0] + " my-column-id org_name")
    sys.exit(1)

project_id = sys.argv[1]
cards_file = project_id + ".csv"
org = sys.argv[2]
token = os.environ['GITHUB_API_TOKEN']

def list_project_cards():
    # Get list of all repos in an org
    response = requests.get(baseurl + "/projects/columns/" + project_id + "/cards", 
        params={'per_page' : 100},
        headers=headers, 
        auth=(org, token))
    if response.status_code != 200:
        # An error occured
        print(COLERR + "Error getting project columns : ",
            + str(response.status_code) + " " + response.text + COLRESET)

    # Convert repos to YAML
    json_cards = json.loads(response.text)
    #print(json.dumps(json_cards, indent=4, sort_keys=True))
    f = open(cards_file, 'w')
    f.write("Issue Key,Summary,Description,Acceptance Criteria,Story Points\n")
    for card in json_cards:
        if not(card["archived"]):
            try:
                issues = requests.get(card["content_url"], 
                    headers=headers, 
                    auth=(org, token))
                json_issues = [json.loads(issues.text)]
                #f.write (f'{json.dumps(json_issue, indent=4, sort_keys=True)}\n')
                for issue in json_issues:
                    f.write (f'{issue["number"]},')
                    f.write (f'{issue["title"]},,,\n')
            except(KeyError):
                print(COLINFO + "Card found that hasn't been converted to an issue:",
                    COLRESET + f'{card["note"]}')
    f.close

list_project_cards()