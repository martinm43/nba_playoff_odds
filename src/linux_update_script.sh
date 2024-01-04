#!/bin/sh
echo "Updating game information"
python update_nba_api.py
echo "Updating game information complete"
python elo_calculator.py
echo "Updates complete, committing changed database"
