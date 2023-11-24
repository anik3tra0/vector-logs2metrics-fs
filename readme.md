# Vector Logs to Metrics to Levitate

This is a way to convert logs to metrics where logs are stored in a File System or Object Store i.e S3, GCS etc. As part of transformation we need to have control over what attributes of json logs need to be considered to be used as dimensions for metrics. These logs need to be seamlessly be converted into metrics in OpenMetrics format and that needs to be remote written to Levitate.

## What does this repo do?
It has a python script that generates logs based on the standard nginx log format which outputs to stdout.

Fluentd listens to stdout and stores these logs as gzipped on the file system.

Vector has a source configuration that reads from the file path where the logs are stored.

Vector parses the log line into json and extracts needed fields.

Vector uses the extracted output and creates metrics out of those.

Vector the uses the metric output and remote writes it to Levitate.

All of this is orchestrated in Docker Compose

## Usage

Clone Repo


```shell
Build everytime you make a change to config.
$ docker-compose up --build -d
```

### Debugging commands

```shell
# To SSH into container
$ docker exec -it log-gen /bin/sh

# To list services/process
$ supervisorctl status

# To check logs of a service/process
$ supervisorctl tail vector # <process_name> as displayed in status command

# This allows you to update config and restart the process instead of rebuilding the container everytime.
# To read/update vector config in container
$ vim /app/vector.yaml

# To restart a process
$ supervisorctl restart vector # <process_name> as displayed in status command

# To tail vector supervisor process
$ tail -f /var/log/supervisor/vector-*.log
```

### Log Generator Usage & Controls

```shell
# Usage
$ python3 ./main.py 1 1

$ python3 ./main.py --help
usage: main.py [-h] num_entries logs_per_minute

Generate random JSON log entries

positional arguments:
  num_entries      Total number of log entries to generate per cycle
  logs_per_minute  Number of log entries to generate per minute

options:
  -h, --help       show this help message and exit
```
