#!/usr/bin/env bash
mkdir -p data
mkdir -p processed

# Get data from archive.org
curl -LO https://archive.org/download/KingBase2018/KingBase2018-pgn.zip
cd data
unzip ../KingBase2028-pgn.zip 

# Process data
./process_data.py
