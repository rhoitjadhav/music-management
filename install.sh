#!/bin/bash

# Exit if any command fails
set -e

# Install Python3
sudo apt install python3

# Install pip
sudo apt install python3-pip

# Install virtualenv
pip3 install --no-cache-dir --user virtualenv

# Create virtualenv
virtualenv -p python3 ./venv

# Activate virtual enviroment
source venv/bin/activate

# Install python packages
pip install --no-cache-dir -r requirements.txt

# Install sqlite3 package
sudo apt install sqlite3

# Create sqlite database file and schema
sqlite3 songs.db < schema.sql

# Create songs_files directory with read/write permissions
mkdir -m 666 songs_files
