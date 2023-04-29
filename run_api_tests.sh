#!/bin/bash

docker-compose -f ./compose-tests.yaml down
rm -rf ./backend/tests/data
docker-compose -f ./compose-tests.yaml up --build -d
echo "waiting for everything to come up (10 sec)"
sleep 10
echo "api tests"
docker exec backend-assignment-api-1 pytest ./tests/test_users.py
echo "unit tests"
docker exec backend-assignment-api-1 pytest ./tests/test_crud.py
docker-compose -f ./compose-tests.yaml down


exit