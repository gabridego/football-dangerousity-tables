# Football dangerousity collector

## Introduction

Leveraging the APIs provided by [Math&Sport](https://www.mathandsport.com/), produce two `csv` tables containing the average maneuvre dangerousity in each match of a football season. Values are also stored, together with other KPIs, in MongoDB collections.

Username and password are required to access a Math&Sport authentication endpoint.

```
usage: main.py [-h] -a AUTH_ENDPOINT -u AUTH_USERNAME -p AUTH_PASSWORD -m MATCH_ENDPOINT [-d [MONGODB_URI]] [-c [CALENDAR_PATH]] [-o [HOME_OUTPUT_PATH]] [-w [AWAY_OUTPUT_PATH]]

Team dangerousity collector

optional arguments:
  -h, --help            show this help message and exit
  -a AUTH_ENDPOINT, --auth-endpoint AUTH_ENDPOINT
                        URL of authentication endpoint
  -u AUTH_USERNAME, --auth-username AUTH_USERNAME
                        Username to access authentication endpoint
  -p AUTH_PASSWORD, --auth-password AUTH_PASSWORD
                        Password to access authentication endpoint
  -m MATCH_ENDPOINT, --match-endpoint MATCH_ENDPOINT
                        URL of endpoint of match statistics
  -d [MONGODB_URI], --mongodb-uri [MONGODB_URI]
                        URI of mongodb host
  -c [CALENDAR_PATH], --calendar-path [CALENDAR_PATH]
                        Path to JSON file containing match information
  -o [HOME_OUTPUT_PATH], --home-output-path [HOME_OUTPUT_PATH]
                        Output path for the file containing dangerousity in home matches
  -w [AWAY_OUTPUT_PATH], --away-output-path [AWAY_OUTPUT_PATH]
                        Output path for the file containing dangerousity in away matches
```

### Project organization

This repository is organized as follows:

```
.
├── data
│   └── calendar.json
├── docker-compose.yml
├── Dockerfile
├── main.py
├── README.md
└── requirements.txt
```

[`data/calendar.json`](./data/calendar.json) is provided by Math&Sport and contains informations about matches of the Italian Serie A, year 2021/22, including match ids that are required to contact their API.

### Table representation

The two produced tables are related to the first and return round of a regular football season. They contain one value for each match and are organized as follows:

- rows correspond to home teams
- collumns correspond to away teams
- cell *(i,j)* contains average dangerousity of home team *i* versus away team *j* (in the match *i vs. j*)

Some cells might be empty, meaning that no statistics was collected for that match.

## Dependencies

Docker can be installed following the [official guide](https://docs.docker.com/engine/install/ubuntu/).

Python requirements are listed in [`requirements.txt`](./requirements.txt) and can be installed running `pip install -r requirements.txt`.

## Instructions

### Run using `docker compose`

Python command line arguments are hardcoded in [`docker-compose.yml`](./docker-compose.yml). Please update it with your credentials for the authentication API.

```
docker compose up -d mongo
docker compose up python
```

To move the generated tables from the container to the host machine, retrieve the python container id using `docker ps -a` and copy the `csv` files to the host:

```
docker cp <container_id>:/usr/src/app/out/home_dangerousity.csv .
docker cp <container_id>:/usr/src/app/out/away_dangerousity.csv .
```

### Run as python script

Run mongo image:

```
docker run -itd -p 27017:27017 --name mongo mongo
```

Run python script:

```
python3 main.py -a https://url/to/auth/api -u username -p password -m https://url/to/match/{id}/api -d mongodb://localhost:27017/
```

## License

Data and APIs are provided by [Math&Sport](https://www.mathandsport.com/), please contact them for information and to access the APIs. All rights reserved.
