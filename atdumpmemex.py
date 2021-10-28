#!/usr/bin/env python3
import base64, json, os, re, requests, sys

# Color constants
# Reference: https://gist.github.com/chrisopedia/8754917
COLERR="\033[0;31m"
COLINFO="\033[0;35m"
COLRESET="\033[m"

graphqlurl = 'https://api.github.com/graphql'
try:
    token = os.environ['GITHUB_API_TOKEN']
except:
    print("Make sure GITHUB_API_TOKEN env variable is set")
    sys.exit()
headers = {"Content-Type": "application/json", 
    "Accept": "application/json",
    "Authorization": "Bearer " + token,
    "GraphQL-Features": "projects_next_graphql" }



def list_memex_projects(org):
    """List the Projects(beta) available in a given org.

    Args:
        org (str): GitHub Organization

    Returns:
        dictionary:
    """
    query = ('query{ organization(login: \\"' + org + '\\") '
        '{ projectsNext(first: 20) { nodes { id number title } } } }')
    response = requests.post(graphqlurl, 
        headers=headers, 
        data='{"query": '+'\"' + query + '\"}')
    if response.status_code != 200:
        # An error occured
        print(COLERR + "Error getting project list : "
            + str(response.status_code) + " " + response.text + COLRESET)

    json_projects = json.loads(response.text)
    return json_projects



def list_memex_columns(project_id):
    """List the columns in a given Projects(beta).

    Args:
        project_id (str): Projects(beta) ID

    Returns:
        dictionary:
    """
    #b64id = base64.b64encode(project_id.encode("ascii")).decode("utf-8")
    query = ('query{ node(id: \\"' + project_id + '\\")  '
        '{ ... on ProjectNext { fields(first: 20) '
        '{ nodes { id name settings } } } } }')
    response = requests.post(graphqlurl, 
        headers=headers, 
        data='{"query": '+'\"' + query + '\"}')
    if response.status_code != 200:
        # An error occured
        print(COLERR + "Error getting project columns : "
            + str(response.status_code) + " " + response.text + COLRESET)
    
    columns = []
    json_nodes = json.loads(response.text)
    for node in json_nodes["data"]["node"]["fields"]["nodes"]:
        if node["name"] == "Status":
            json_status = json.loads(node["settings"])
            for options in json_status["options"]:
                columns.append(str(options["id"])+' '+options["name"])
    return columns
            


def list_memex_cards(column_id, project_id):
    """Export the cards in a Projects(beta) column to .csv.

    Args:
        column_id (str): Column ID
        project_id (str): Projects(beta) ID
    """
    cards_file = column_id + ".csv"
    #b64id = base64.b64encode(project_id.encode("ascii")).decode("utf-8")
    query = ('query{ node(id: \\"' + project_id + '\\") '
        '{ ... on ProjectNext { items(first: 100) '
        '{ nodes{ title fieldValues(first: 8) { nodes{ value } } '
        'content{ ...on Issue { number labels(first: 50) '
        '{ nodes{ name } } } } } } } } }')
    response = requests.post(graphqlurl, 
        headers=headers, 
        data='{"query": '+'\"' + query + '\"}')
    if response.status_code != 200:
        # An error occured
        print(COLERR + "Error getting project column cards : "
            + str(response.status_code) + " " + response.text + COLRESET)

    json_cards = json.loads(response.text)
    f = open(cards_file, 'w')
    f.write("Issue Key,Summary,Description,Acceptance Criteria,Story Points\n")
    for card in json_cards["data"]["node"]["items"]["nodes"]:
        for status in card["fieldValues"]["nodes"]:
            if status["value"] == column_id:
                # Remove special chars and limit length to 80 chars
                title = re.sub('[^A-Za-z0-9.@ ]+', '', card["title"])[:80]
                f.write(f'{card["content"]["number"]},{title},,,')
                for label in card["content"]["labels"]["nodes"]:
                        if (label["name"][-2:]=="SP"):
                            f.write (f'{label["name"].partition(" ")[0]}')
                            # break loop in case there are multiple SP labels
                            break
                f.write ('\n')
    f.close