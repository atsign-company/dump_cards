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

### list_projects.py

Lists the project IDs, numbers and title for projects in a given (presently
hard coded) organization.
`./list_projects.py`

### list_project_columns.py

Lists the column IDs and Names from a given (presently hard coded) project ID
`./list_project_columns.py`

### dump_project_cards.py

Dump the issue number and title from the cards in a given column:  
`./dump_project_cards.py 11235813`