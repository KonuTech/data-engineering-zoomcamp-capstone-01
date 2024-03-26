#!/bin/bash

# Stop and remove all Docker containers
docker stop $(docker ps -aq) && docker rm $(docker ps -aq)
