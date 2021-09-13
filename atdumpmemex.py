#!/usr/bin/env python3
import os, json, requests, base64

# Color constants
# Reference: https://gist.github.com/chrisopedia/8754917
COLERR="\033[0;31m"
COLINFO="\033[0;35m"
COLRESET="\033[m"

graphqlurl = 'https://api.github.com/graphql'
# Use inertia-preview for List project cards API to see archived cards
token = os.environ['GITHUB_API_TOKEN']
headers = {"Content-Type": "application/json", 
    "Accept": "application/vnd.github.jean-grey-preview+json",
    "Authorization": "Bearer " + token,
    "GraphQL-Features": "projects_next_graphql" }

def list_memex_projects(org):
    query = 'query{ organization(login: \\"' + org + '\\") { projectsNext(first: 20) { nodes { id title } } } }'
    response = requests.post(graphqlurl, 
        headers=headers, 
        data='{"query": '+'\"' + query + '\"}')
    if response.status_code != 200:
        # An error occured
        print(COLERR + "Error getting project list : "
            + str(response.status_code) + " " + response.text + COLRESET)

    json_projects = json.loads(response.text)
    #print(json.dumps(json_cards, indent=4, sort_keys=True))
    project_id = base64.b64decode(json_projects["data"]["organization"]["projectsNext"]["nodes"][0]["id"])
    print(f'{project_id.decode("utf-8")} ' 
        + f'{json_projects["data"]["organization"]["projectsNext"]["nodes"][0]["title"]}')

def list_memex_columns(project_id):
    b64id = base64.b64encode(project_id.encode("ascii")).decode("utf-8")
    query = 'query{ node(id: \\"' + b64id + '\\")  { ... on ProjectNext { fields(first: 20) { nodes { id name settings } } } } }'
    response = requests.post(graphqlurl, 
        headers=headers, 
        data='{"query": '+'\"' + query + '\"}')
    if response.status_code != 200:
        # An error occured
        print(COLERR + "Error getting project columns : "
            + str(response.status_code) + " " + response.text + COLRESET)
    
    json_nodes = json.loads(response.text)
    for node in json_nodes["data"]["node"]["fields"]["nodes"]:
        if node["name"] == "Status":
            json_status = json.loads(node["settings"])
            for options in json_status["options"]:
                print(f'{options["id"]} {options["name"]}')
            


def list_memex_cards(column_id, project_id):
    cards_file = column_id + ".csv"
    b64id = base64.b64encode(project_id.encode("ascii")).decode("utf-8")
    query = 'query{ node(id: \\"' + b64id + '\\") { ... on ProjectNext { items(first: 100) { nodes{ title fieldValues(first: 8) { nodes{ value } } content{ ...on Issue { number labels(first: 50) { nodes{ name } } } } } } } } }'
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
                f.write(f'{card["content"]["number"]},{card["title"]},,,')
                for label in card["content"]["labels"]["nodes"]:
                        if (label["name"][-2:]=="SP"):
                            f.write (f'{label["name"].partition(" ")[0]}')
                            # break loop in case there are multiple SP labels
                            break
                f.write ('\n')
    f.close