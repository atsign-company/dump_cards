#!/usr/bin/env python3
import base64
import json
import os
import re
import sys

import requests
import dotenv

# Color constants
# Reference: https://gist.github.com/chrisopedia/8754917
COLERR = "\033[0;31m"
COLINFO = "\033[0;35m"
COLRESET = "\033[m"

graphqlurl = 'https://api.github.com/graphql'

DUMP_CARDS_PATH = os.getcwd()
DOTENV_PATH = f"{DUMP_CARDS_PATH}/.env"

dotenv.load_dotenv(DOTENV_PATH)

try:
    token = os.environ['GITHUB_API_TOKEN']
except:
    print("Make sure GITHUB_API_TOKEN env variable is set")
    sys.exit()

headers = {"Content-Type": "application/json",
           "Accept": "application/json",
           "Authorization": "Bearer " + token,
           "GraphQL-Features": "projects_next_graphql"}


def list_v2_projects(org):
    """List the Projects(V2) available in a given org.

    Args:
        org (str): GitHub Organization

    Returns:
        dictionary:
    """
    query = ('query{ organization(login: \\"' + org + '\\") '
             '{ projectsV2(first: 20) { nodes { id number title closed } } } }')
    response = requests.post(graphqlurl,
                             headers=headers,
                             data='{"query": '+'\"' + query + '\"}')
    if response.status_code != 200:
        # An error occured
        print(COLERR + "Error getting project list : "
              + str(response.status_code) + " " + response.text + COLRESET)

    json_projects = json.loads(response.text)
    return json_projects


def list_v2_fields(project_id):
    """List the fields in a given Projects(V2). (SingleSelection/Iteration Fields Only)
    Args:
        project_id (str): Projects(V2) ID

    Returns:
        dictionary:
    """
    # b64id = base64.b64encode(project_id.encode("ascii")).decode("utf-8")
    query = ('query{ node(id: \\"' + project_id + '\\")  '
             '{ ... on ProjectV2 { fields(first: 20) '
             '{ nodes { ...on ProjectV2IterationField { id name }'
             '...on ProjectV2SingleSelectField { id name } } } } } }')
    response = requests.post(graphqlurl,
                             headers=headers,
                             data='{"query": '+'\"' + query + '\"}')
    if response.status_code != 200:
        # An error occured
        print(COLERR + "Error getting project columns : "
              + str(response.status_code) + " " + response.text + COLRESET)

    fields = []
    json_nodes = json.loads(response.text)
    for node in json_nodes["data"]["node"]["fields"]["nodes"]:
        if node.get("id") is None:
            continue
        fields.append(str(node["id"])+' '+node["name"])
    return fields


def list_v2_columns(field_id):
    """List the columns of a field in a given Projects(V2). (SingleSelection/Iteration Fields Only)

    Args:
        field_id (str): Projects(V2) ID
    Returns:
        dictionary:
    """
    # b64id = base64.b64encode(project_id.encode("ascii")).decode("utf-8")
    query = ('query{ node(id: \\"' + field_id + '\\")  '
             '{ ...on ProjectV2IterationField { configuration { iterations { title } } }'
             '...on ProjectV2SingleSelectField { options { name } } } }')
    response = requests.post(graphqlurl,
                             headers=headers,
                             data='{"query": '+'\"' + query + '\"}')
    if response.status_code != 200:
        # An error occured
        print(COLERR + "Error getting project columns : "
              + str(response.status_code) + " " + response.text + COLRESET)

    columns = []
    json_nodes = json.loads(response.text)
    node = json_nodes["data"]["node"]
    if node.get("configuration") != None:
        for iteration in node["configuration"]["iterations"]:
            columns.append(iteration["title"])
    elif node.get("options") != None:
        for option in node["options"]:
            columns.append(option["name"])
    return columns


def list_v2_cards(field_id, project_id, column_name, file_name=None):
    """Export the cards in a Projects(V2) column to .csv.

    Args:
        field_id (str): Projects(V2) field ID
        project_id (str): Projects(V2) ID
        column_name (str): Column name
        file_name (str): Name of the file to export to (without the extension). Defaults to column_id.
    """
    if file_name is None:
        file_name = column_name
    cards_file = file_name + ".csv"
    # b64id = base64.b64encode(project_id.encode("ascii")).decode("utf-8")
    getPage = True
    cursor = ""
    f = open(cards_file, 'w')
    f.write("Issue Key,Summary,Description,Acceptance Criteria,Story Points\n")
    while getPage:
        query = ('query{ node(id: \\"' + project_id + '\\") '
                 '{ ... on ProjectV2 { items(first: 100 ' + cursor + ') '
                 '{ pageInfo { hasNextPage endCursor}'
                 ' nodes{  content { ...on Issue { number title }'
                 '...on DraftIssue { title }'
                 '...on PullRequest { number title }'
                 '} fieldValues(first: 20) { nodes {'
                 '...on ProjectV2ItemFieldNumberValue { field { ...on ProjectV2FieldCommon { id name } } number }'
                 '...on ProjectV2ItemFieldSingleSelectValue { field { ...on ProjectV2FieldCommon { id name } } name }'
                 '...on ProjectV2ItemFieldIterationValue { field { ...on ProjectV2FieldCommon { id  name } } title } } } } } } } }')

        response = requests.post(graphqlurl,
                                 headers=headers,
                                 data='{"query": '+'\"' + query + '\"}')
        if response.status_code != 200:
            # An error occured
            print(COLERR + "Error getting project column cards : "
                  + str(response.status_code) + " " + response.text + COLRESET)

        json_cards = json.loads(response.text)
        for card in json_cards["data"]["node"]["items"]["nodes"]:
            correctColumn, title, number, sp, status = None, None, None, None, None
            for fieldValue in card["fieldValues"]["nodes"]:
                if fieldValue.get('field') != None and fieldValue['field']['id'] == field_id:
                    correctColumn = (fieldValue.get('name') != None and fieldValue['name'] == column_name or
                                     fieldValue.get('title') != None and fieldValue['title'] == column_name)
                    if correctColumn == False:
                        break
                if (fieldValue.get('field') != None and (fieldValue['field']['name'].lower() == "sp" or fieldValue['field']['name'].lower() == "sprint points")):
                    sp = fieldValue.get('number')
                    sp = int(sp) if sp != None else None
                if (fieldValue.get('field') != None and (fieldValue['field']['name'].lower() == "status")):
                    status = fieldValue.get('name')
            if(status == 'Closed'):
                continue
            elif(status == 'Active'):
                status = ''
            else:
                status = f'[{status}] '
            if(correctColumn):
                if card.get("content") == None:
                    title = "ERROR READING PRIVATE ISSUE"
                if card != None:
                    title = card.get("content", dict()).get("title", "")
                    # Remove special chars and limit length to 80 chars
                    title = re.sub('[^A-Za-z0-9.@ ]+', '', title)[:80]
                number = card["content"].get("number")
                if number == None:
                    f.write(f'Draft,{status}{title},,,{sp}\n')
                else:
                    f.write(f'{number},{status}{title},,,{sp}\n')
        getPage = json_cards["data"]["node"]["items"]["pageInfo"]["hasNextPage"]
        cursor = 'after:\\"' + \
            json_cards["data"]["node"]["items"]["pageInfo"]["endCursor"] + '\\"'
    f.close()
