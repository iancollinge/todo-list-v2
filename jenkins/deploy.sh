#!/bin/bash

echo "Deploy stage"

scp docker-compose.yaml jenkins@swarm-manager:/home/jenkins/docker-compose.yaml
ssh jenkins@swarm-manager docker stack deploy --compose-file docker-compose.yaml todo-app
