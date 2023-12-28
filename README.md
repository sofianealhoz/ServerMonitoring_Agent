# agent-py

## Requirements

- Python 3.X
- virtualenv [intall](https://virtualenv.pypa.io/en/latest/installation.html)

## Run project

```sh
make environment
make help
make run
#or
make debug
```

## Configuration

Environment variable:

- AGENT_ENV: local/production
- AGENT_VERSION: app version, default 1.0.0, endpoint /version
- AGENT_DESCRIPTION: app description
- AGENT_DEBUG: activate debug mode (boolean)

local : enable reload mode (default)
prod : no hot reload

## Usage

Run project with `make debug` and consult url in log for api doc at `/docs` or `/redoc`.

Application is running 2 threads, one for the API to expose metrics and one for collecting metrics.
 
## Description

A tool for monitoring servers was created with the following functionalities:

Establishing connections to designated machines.
Retrieving CPU and RAM information from these remote machines.
Extracting information from logs on the monitored machines.
Implementing continuous delivery for the project through a Docker image.
This project was developed within a DevOps framework, ensuring adherence to the following practices:

Writing tests and executing them with every push.
Implementing continuous integration.
Employing a linter for code quality checks.
Calculating and analyzing code coverage statistics.






## Installation
To run this project all you need is to pull & run our Docker image :

To run the docker image that contains our project, run the following commands :

```bash
docker login
```
The username is: ...

The password is: ...

```bash
docker pull ...
```
```bash
docker run -p ...
```

## Built With
* Python
* Docker
* Dart

