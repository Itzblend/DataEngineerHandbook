#!/bin/bash

# Check if the container exists
if [ "$(docker ps -a -q -f name=azurite_storage)" ]; then
    echo "Container azurite_storage exists. Starting it..."
    docker start azurite_storage
else
    echo "Container azurite_storage does not exist. Creating it..."
    docker run -d -p 10000:10000 -p 10001:10001 --name azurite_storage -v /var/azurite:/data mcr.microsoft.com/azure-storage/azurite:latest
fi

