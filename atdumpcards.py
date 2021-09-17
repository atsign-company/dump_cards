import os, json, requests, sys

# Color constants
# Reference: https://gist.github.com/chrisopedia/8754917
COLERR="\033[0;31m"
COLINFO="\033[0;35m"
COLRESET="\033[m"

baseurl = 'https://api.github.com'
try:
    token = os.environ['GITHUB_API_TOKEN']
except:
    print("Make sure GITHUB_API_TOKEN env variable is set")
    sys.exit()
# Use inertia-preview for List project cards API to see archived cards
headers = {"Content-Type": "application/json", 
    "Accept": "application/vnd.github.inertia-preview+json",
    "Authorization": "Bearer " + token}


def list_orgs():
    """Get a list of orgs for the authenticated user (from token).

    Args:
        token (str): GitHub API Token

    Returns:
        dictionary:
    """
    response = requests.get(baseurl + "/user/memberships/orgs", 
        headers=headers)
    if response.status_code != 200:
        # An error occured
        print(COLERR + "Error getting project list : "
            + str(response.status_code) + " " + response.text + COLRESET)

    json_orgs = json.loads(response.text)
    return json_orgs


def list_projects(org):
    """Get list of all projects in an org.

    Args:
        org (str): GitHub Organization

    Returns:
        dictionary:
    """
    response = requests.get(baseurl + "/orgs/" + org + "/projects", 
        headers=headers)
    if response.status_code != 200:
        # An error occured
        print(COLERR + "Error getting project list : "
            + str(response.status_code) + " " + response.text + COLRESET)

    json_projects = json.loads(response.text)
    return json_projects
    

def list_project_columns(project_id):
    """Get list of all columns for a project.

    Args:
        project_id (str): Project ID

    Returns:
        dictionary:
    """
    response = requests.get(baseurl + "/projects/" + project_id + "/columns", 
        headers=headers)
    if response.status_code != 200:
        # An error occured
        print(COLERR + "Error getting project columns : "
            + str(response.status_code) + " " + response.text + COLRESET)

    json_columns = json.loads(response.text)
    return json_columns
    

def list_project_cards(column_id):
    """Export the cards in a Project column to .csv.

    Args:
        column_id (str): Column ID
    
    Note:
        This doesn't deal with paging, so presently limited to 100 cards
    """
    cards_file = column_id + ".csv"
    response = requests.get(baseurl + "/projects/columns/" 
        + column_id + "/cards", 
        params={'per_page' : 100},
        headers=headers)
    if response.status_code != 200:
        # An error occured
        print(COLERR + "Error getting project column cards : "
            + str(response.status_code) + " " + response.text + COLRESET)

    json_cards = json.loads(response.text)
    #print(json.dumps(json_cards, indent=4, sort_keys=True))
    f = open(cards_file, 'w')
    f.write("Issue Key,Summary,Description,Acceptance Criteria,Story Points\n")
    for card in json_cards:
        if not(card["archived"]):
            try:
                issues = requests.get(card["content_url"], 
                    headers=headers)
                json_issues = [json.loads(issues.text)]
                for issue in json_issues:
                    f.write (f'{issue["number"]},{issue["title"]},,,')
                    # Extract story points if present in labels like `3 SP`
                    for label in issue["labels"]:
                        if (label["name"][-2:]=="SP"):
                            f.write (f'{label["name"].partition(" ")[0]}')
                            # break loop in case there are multiple SP labels
                            break
                    f.write ('\n')
            except(KeyError):
                print(COLINFO 
                    + "Card found that hasn't been converted to an issue:",
                    COLRESET + f'{card["note"]}')
    f.close