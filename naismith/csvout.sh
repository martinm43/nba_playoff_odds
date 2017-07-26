#!/data/data/com.termux/files/usr/bin/sh
#Change the above to $PATH for the relevant Linux system
sqlite3 nba_data_test.sqlite < csvout.txt
cp trimatch.csv sqlcsv
