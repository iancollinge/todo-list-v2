#!/bin/bash

echo "Deploy stage"

ssh jenkins@swarm-manager docker stack deploy --compose-file docker-compose.yaml todo-app
