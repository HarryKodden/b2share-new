
## Steps to prepare for tests:

### Prepare support services
(NOTE: You might occasionally want to run `docker-compose down -v` between test to get rid of bad state of e.g. Postgres or Elasticsearch)

`$ docker-compose -f docker-compose-dev.yml up -d`


### Prepare environment

- NOTES:
  *`[all]` should install dependencies required by testing

`$ pip install -e .[all]`


## Execute tests

- NOTES:
  * `-s` flag prevents Pytest from capturing 'stdout' and 'stderr'
  * `-vvv` might be too much debug info. Reduce verbosity if needed.
  * conftest.py should be picked up by Pytest automatically

`$ pytest -svvv tests/b2share_unit_tests/`

# Test in VSCode

## Prepare Virtual Environment

```
python3.6 -m venv .venv
source .venv/bin/activate
pip install --upgrade-pip
pip install poetry
poetry update
```

## Prepare VScode

Make sure you have have .vscode/settings.json and .vscode/lauch.json in proper shape:

.vscode/settings.json
```
{ 
  "python.testing.unittestEnabled": false,
    "python.testing.nosetestsEnabled": false,
    "python.testing.pytestEnabled": true,
    "python.pythonPath": "${workspaceFolder}/.venv/bin/python",
    "python.testing.pytestArgs": [
        "--no-cov"
    ],
    "python.venvPath": "${workspaceFolder}/.venv",
    "python.envFile": "${workspaceFolder}/.env"
}
```

.vscode/launch.json
```
{
    // Use IntelliSense to learn about possible attributes.
    // Hover to view descriptions of existing attributes.
    // For more information, visit: https://go.microsoft.com/fwlink/?linkid=830387
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Current File",
            "type": "python",
            "request": "launch",
            "program": "${file}",
            "console": "integratedTerminal"
        }
    ]
}
```

