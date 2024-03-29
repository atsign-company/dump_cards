## Python scripts (old style projects):

These scripts use the v3 REST API, making use of functions in the
[atdumpcards.py](atdumpcards.py) module.

### list_projects.py

Lists the project IDs, numbers and title for projects in a given organization.  
`./list_projects.py my-organisation`

Example output:  
```
$ ./list_projects.py atsign-foundation
6018453 3 Sprint Planning Project Board
11987336 4 @mosphere Project Board
12437918 5 App Launch  & Developer Traction
12961019 7 Flutter packages board
```

### list_project_columns.py

Lists the column IDs and Names from a given project ID  
`./list_project_columns.py my-project-id`

Example output:  
```
./list_project_columns.py 6018453
11918750 Backlog
12092381 Bugs
14337222 PR12 - 107 SP's (Capacity 105)
13742763 Spike - POC
```

### dump_project_cards.py

Dump the issue number, title and story points from the cards in a given
column:  
`./dump_project_cards.py my-column-id`

Example usage:
```
$ ./dump_project_cards.py 11235813
```

Example file content:
```
$cat 11235813.csv
Issue Key,Summary,Description,Acceptance Criteria,Story Points
38,Integrate Rocky's design into Docsy WTF site,,,1
43,Home/landing page messaging and content,,,
40,Docs Page - Left hand menu items and flow,,,
41,Landing page design for each of main category pages in the top menu,,,
46,Open Source Policies & Process,,,5
45,Update Nomenclature on Pub.dev and other pages,,,3
```

## Python scripts - Projects (beta)

These scripts use the v4 GraphQL API to access projects from Projects (beta)
aka ProjectsNext aka Memex aka Issues feature, making use of functions in
the [atdumpmemex.py](atdumpmemex.py) module.

### list_nextprojects.py

Lists the project IDs, numbers and title for projects in a given organization.  
`./list_nextprojects.py my-organisation`

Example output:
```
$ ./list_nextprojects.py atsign-company
011:ProjectNext3594 E2E3 @ Hack - Moving to Oct 22nd?
```

### list_nextproject_columns.py

`./list_nextproject_columns.py my-project-id`

Example output:

```
$ ./list_nextproject_columns.py 011:ProjectNext3594
f75ad846 To Do - Yet to Start
47fc9ee4 PR19.5 14 SP's | 15 Velocity (1 over)
98236657 Done
```

### dump_nextproject_cards.py

Dump the issue number, title and story points from the cards in a given
column:  
`./dump_nextproject_cards.py my-project-id column-id`

Example usage:
```
$ ./dump_nextproject_cards.py 011:ProjectNext3594 47fc9ee4
```

Example file content:
```
$ cat 47fc9ee4.csv
Issue Key,Summary,Description,Acceptance Criteria,Story Points
34,Finalize the new dates for @Hack,,,2
32,Marketing and Promotions,,,3
30,Identify Key Note Speakers and other speaking sessions,,,2
31,Finalize Tracks and Sponsors,,,2
22,Platform (Tool) for Hosting the @Hack,,,1
26,Discord Setup for @Hack,,,2
23,Mentors for the various tracks,,,2
28,Judging Panel for the tracks,,,1
```

## Hard coded scripts

A number of the scripts are hard coded to atsign-company and atsign-foundation:

### list_company.py

Lists the projects by ID in atsign-company org.  
`./list_company.py`

### list_foundation.py

Lists the projects by ID in atsign-foundation org.  
`./list_foundation.py`

### list_atsigndev_columns.py
Lists the column IDs and Names from the atsign-foundation atsign.dev
project.  
`./list_atsigndev_columns.py`

### list_e2e3‎@hack_columns.py
Lists the column IDs and Names from the atsign-company E2E3 @Hack
project.  
`./list_e2e3@hack_columns.py`

### list_marketing_columns.py
Lists the column IDs and Names from the atsign-company marketing
project.  
`./list_marketing_columns.py`

### list_sprintplanning_columns.py
Lists the column IDs and Names from the atsign-foundation sprint planning
project.  
`./list_sprintplanning_columns.py`

### dump_company_cards.py

Dump the issue number and title from the cards in a given column within
atsign-company boards.
`./dump_company_cards.py 11235813`

### dump_foundation_cards.py

Dump the issue number and title from the cards in a given column within
atsign-foundation boards.
`./dump_foundation_cards.py 11235813`