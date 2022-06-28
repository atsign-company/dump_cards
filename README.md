<img width=250px src="https://atsign.dev/assets/img/atPlatform_logo_gray.svg?sanitize=true">

# dump\_cards
Repo to dump cards from a project column into a CSV file that can be imported
into [planningpoker.com](https://www.planningpoker.com/).

[![GitHub License](https://img.shields.io/badge/license-Apache2-blue.svg)](https://www.apache.org/licenses/LICENSE-2.0) 

## Contributions:

If you find a bug then please raise an
[issue](https://github.com/atsign-company/dump_cards/issues).

We'd also love to get [pull requests](https://github.com/atsign-company/dump_cards/pulls)
for improvements.

Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details.

Our [code of conduct](code_of_conduct.md) is based on
[![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-2.0-4baaaa.svg)](code_of_conduct.md)

## Security token

These scripts need a security token with access to read:org

![image](https://user-images.githubusercontent.com/478926/133479440-04abd22f-d3c3-4082-90ad-1431898839ce.png)

The token should be in an environment variable `GITHUB_API_TOKEN`

An easy way to do this is set it in a `.env` file:

```
# ./.env
# API keys for GitHub etc.
GITHUB_API_TOKEN=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 # <- put your token here
# ^ this token was deleted already so it needs to be replaced
```

## Interactive script

This project uses the
[InquirerPy](https://pypi.org/project/inquirerpy/),
[python-dotenv](https://pypi.org/project/python-dotenv/) and
[requests](https://pypi.org/project/requests/) modules, so you need to
install them:

```
pip3 install InquirerPy
pip3 install python-dotenv
pip3 install requests
```

Or, by using the `requirements.txt`:

```
pip3 install -r requirements.txt
```

Then run:

```
./dump_cards.py
```

The menus will then prompt for selection of org, project type, and column
before exporting the column to .csv

[![asciicast](https://asciinema.org/a/zWE8AisDzacCKqlGpdu7dwPqO.svg)](https://asciinema.org/a/zWE8AisDzacCKqlGpdu7dwPqO)

## Shell script

### merge.sh

This is used to merge the latest two files (which should be .csv files) so
that the headers from the second file are stripped out in order to create
a single file that can be imported to Planning Poker.  
`./merge.sh`
