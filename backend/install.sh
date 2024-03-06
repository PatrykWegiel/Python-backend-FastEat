#!/bin/bash

if [ "$#" -lt 1 ]; then
    echo "Backend install & update script usage: $0 [packages|pip|virtualenv|hosts]"
    exit
fi

ACTIVE=$(git rev-parse --abbrev-ref HEAD)
echo "Active branch: $ACTIVE"

case $1 in
    "packages")
        apt-get update -q
        apt-get install -y -q \
            apt-transport-https \
            build-essential \
            ca-certificates \
            git-core \
            libffi-dev \
            libssl-dev \
            libpq-dev \
            python3-dev \
            python3-pip \
            python3-virtualenv \
            binutils \
            libproj-dev \
            gdal-bin \
            zip \
            postgresql-client

        pip3 install pip --upgrade
        ;;
    "virtualenv")
        virtualenv -p python3 .venv
        ;;
    "pip")
        pip3 install -r requirements.txt
        ;;
    "hosts")
        echo '127.0.0.1 db' >> /etc/hosts
        echo '127.0.0.1 redis' >> /etc/hosts
        ;;
esac