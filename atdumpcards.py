import os, sys, json, requests, yaml

# Color constants
# Reference: https://gist.github.com/chrisopedia/8754917
COLERR="\033[0;31m"
COLINFO="\033[0;35m"
COLRESET="\033[m"

baseurl = 'https://api.github.com'
headers = {"Content-Type": "application/json", "Accept": "application/vnd.github.inertia-preview+json"}
token = os.environ['GITHUB_API_TOKEN']

def list_projects(org):
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

def list_project_columns(project_id, org):
    # Get list of all repos in an org
    response = requests.get(baseurl + "/projects/" + project_id + "/columns", 
        headers=headers, 
        auth=(org, token))
    if response.status_code != 200:
        # An error occured
        print(COLERR + "Error getting project columns : " + str(response.status_code) + " " + response.text
        + COLRESET)

    # Convert repos to YAML
    json_projects = json.loads(response.text)
    #print(json.dumps(json_project, indent=4, sort_keys=True))
    for project in json_projects:
        print(f'{project["id"]} {project["name"]}')

def list_project_cards(column_id, org):
    cards_file = column_id + ".csv"
    # Get list of all repos in an org
    response = requests.get(baseurl + "/projects/columns/" + column_id + "/cards", 
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
                for issue in json_issues:
                    f.write (f'{issue["number"]},{issue["title"]},,,')
                    for label in issue["labels"]:
                        if (label["name"][-2:]=="SP"):
                            f.write (f'{label["name"].partition(" ")[0]}')
                            break
                    f.write ('\n')
            except(KeyError):
                print(COLINFO + "Card found that hasn't been converted to an issue:",
                    COLRESET + f'{card["note"]}')
    f.close

