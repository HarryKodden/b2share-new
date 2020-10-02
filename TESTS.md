
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


