<img src="https://atsign.dev/assets/img/@dev.png?sanitize=true">

### Now for a little internet optimism

# dump_cards
Repo to dump cards from a project column into a CSV file that can be imported
into [planningpoker.com](https://www.planningpoker.com/).

## LICENSE:

[Apache License Version 2.0](https://www.apache.org/licenses/LICENSE-2.0) 

## Contributions:

If you find a bug then please raise an [issue](https://github.com/atsign-company/dump_cards/issues).

We'd also love to get [pull requests](https://github.com/atsign-company/dump_cards/pulls)
for improvements.

Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details.

Our [code of conduct](code_of_conduct.md) is based on
[![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-2.0-4baaaa.svg)](code_of_conduct.md)

## Python scripts:

All scripts are presently hard coded to use `atsign-foundation` organization.
But this can be replaced by passing in a command line argument (see commented
lines).

### list_projects.py

Lists the project IDs, numbers and title for projects in a given organization.
`./list_projects.py my-organisation`

Example output:  
```
6018453 3 Used for tracking backlogs, bugs, issues, enhancements across multiple repo's in Open Source.
11987336 4 Used for tracking backlogs, bugs, issues, enhancements across multiple repo's in Open Source.
12437918 5 Open source development and sprint planning for https://atsign.dev.
```

### list_project_columns.py

Lists the column IDs and Names from a given project ID  
`./list_project_columns.py 21345589 my-organisation`

Example output:  
```
11918750 Backlog
12092381 Bugs
14337222 PR12 - 107 SP's (Capacity 105)
13742763 Spike - POC
```

### dump_project_cards.py

Dump the issue number and title from the cards in a given column:  
`./dump_project_cards.py 11235813 my-organisation`

Example file content:
```
Issue Key,Summary,Description,Acceptance Criteria,Story Points
38,Integrate Rocky's design into Docsy WTF site,,,
43,Home/landing page messaging and content,,,
40,Docs Page - Left hand menu items and flow,,,
41,Landing page design for each of main category pages in the top menu,,,
46,Open Source Policies & Process,,,
45,Update Nomenclature on Pub.dev and other pages,,,
```

## Hard coded scripts

A number of the scripts are hard coded to atsign-company and atsign-foundation:

### list_company.py

Lists the projects by ID in atsign-company org.

### list_foundation.py

Lists the projects by ID in atsign-compafoundationny org.

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
`/dump_company_cards.py 11235813`

### dump_foundation_cards.py

Dump the issue number and title from the cards in a given column within
atsign-foundation boards.
`/dump_foundation_cards.py 11235813`