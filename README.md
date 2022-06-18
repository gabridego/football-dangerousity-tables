## Run script

```
python3 main.py -a https://url/to/auth/api -u username -p password -m https://url/to/match/{id}/api
```

```
usage: main.py [-h] -a AUTH_ENDPOINT -u AUTH_USERNAME -p AUTH_PASSWORD -m MATCH_ENDPOINT [-c [CALENDAR_PATH]] [-o [HOME_OUTPUT_PATH]] [-w [AWAY_OUTPUT_PATH]]

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
  -c [CALENDAR_PATH], --calendar-path [CALENDAR_PATH]
                        Path to JSON file containing match information
  -o [HOME_OUTPUT_PATH], --home-output-path [HOME_OUTPUT_PATH]
                        Output path for the file containing dangerousity in home matches
  -w [AWAY_OUTPUT_PATH], --away-output-path [AWAY_OUTPUT_PATH]
                        Output path for the file containing dangerousity in away matches
```

## Run container

```
sudo docker build -t mathsport:latest .
sudo docker run -it mathsport -a https://url/to/auth/api -u username -p password -m https://url/to/match/{id}/api
```

Get container id:

```
sudo docker ps -a
```

Copy files to host:

```
sudo docker cp <container_id>:/usr/src/app/out/home_dangerousity.csv .
sudo docker cp <container_id>:/usr/src/app/out/away_dangerousity.csv .
```