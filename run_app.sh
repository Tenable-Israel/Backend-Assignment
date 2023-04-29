#!/usr/bin/env bash

docker-compose -f ./compose-tests.yaml down
docker-compose -f ./compose-tests.yaml up --build -d