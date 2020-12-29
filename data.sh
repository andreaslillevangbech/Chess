#!/usr/bin/env bash
mkdir -p data
mkdir -p processed

# Get data from archive.org
cd data
curl -LO https://archive.org/download/KingBase2018/KingBase2018-pgn.zip
cd ..

# Process data
./get_data.py
